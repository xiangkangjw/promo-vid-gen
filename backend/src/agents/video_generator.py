from typing import Dict, Any, List
import asyncio
import os
import tempfile
import requests
from elevenlabs import generate, save
import ffmpeg
from src.core.base_agent import BaseAgent

class VideoGeneratorAgent(BaseAgent):
    """
    Generates visuals, voiceover, and assembles final video
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("VideoGeneratorAgent", config)
        self.elevenlabs_api_key = self.config.get("elevenlabs_api_key", "")
        self.pexels_api_key = self.config.get("pexels_api_key", "")
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final promotional video
        
        Args:
            input_data: {
                "script": str,
                "scenes": List[Dict],
                "restaurant_name": str,
                "style": str
            }
            
        Returns:
            {
                "video_path": str,
                "thumbnail_path": str,
                "duration": float,
                "file_size": int,
                "resolution": str
            }
        """
        self.validate_input(input_data, ["script", "scenes", "restaurant_name"])
        
        try:
            script = input_data["script"]
            scenes = input_data["scenes"]
            restaurant_name = input_data["restaurant_name"]
            style = input_data.get("style", "casual")
            
            self.log_progress(f"Generating video for {restaurant_name}")
            
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                
                # Step 1: Generate voiceover
                audio_path = await self._generate_voiceover(script, temp_dir)
                
                # Step 2: Download/generate images for each scene
                image_paths = await self._generate_scene_images(scenes, temp_dir)
                
                # Step 3: Assemble final video
                video_path = await self._assemble_video(
                    audio_path, image_paths, scenes, temp_dir, restaurant_name
                )
                
                # Step 4: Generate thumbnail
                thumbnail_path = await self._generate_thumbnail(video_path, temp_dir)
                
                # Step 5: Get video metadata
                metadata = await self._get_video_metadata(video_path)
                
                self.log_progress("Video generation completed")
                
                return {
                    "video_path": video_path,
                    "thumbnail_path": thumbnail_path,
                    "duration": metadata["duration"],
                    "file_size": metadata["file_size"],
                    "resolution": metadata["resolution"]
                }
                
        except Exception as e:
            self.log_progress(f"Error generating video: {str(e)}", "error")
            raise
    
    async def _generate_voiceover(self, script: str, temp_dir: str) -> str:
        """
        Generate voiceover audio using ElevenLabs
        """
        try:
            self.log_progress("Generating voiceover")
            
            # Generate audio using ElevenLabs
            audio = generate(
                text=script,
                voice="Bella",  # Default voice
                api_key=self.elevenlabs_api_key
            )
            
            audio_path = os.path.join(temp_dir, "voiceover.mp3")
            save(audio, audio_path)
            
            return audio_path
            
        except Exception as e:
            self.log_progress(f"Voiceover generation failed: {str(e)}", "warning")
            # Return silent audio as fallback
            return await self._generate_silent_audio(temp_dir, 30)  # 30 seconds
    
    async def _generate_scene_images(self, scenes: List[Dict], temp_dir: str) -> List[str]:
        """
        Download or generate images for each scene
        """
        image_paths = []
        
        for i, scene in enumerate(scenes):
            try:
                image_prompt = scene.get("image_prompt", "restaurant food")
                
                # Download image from Pexels
                image_path = await self._download_stock_image(
                    image_prompt, f"scene_{i}.jpg", temp_dir
                )
                
                image_paths.append(image_path)
                
            except Exception as e:
                self.log_progress(f"Failed to get image for scene {i}: {str(e)}", "warning")
                # Use placeholder image
                placeholder_path = await self._create_placeholder_image(temp_dir, f"scene_{i}.jpg")
                image_paths.append(placeholder_path)
        
        return image_paths
    
    async def _download_stock_image(self, query: str, filename: str, temp_dir: str) -> str:
        """
        Download stock image from Pexels
        """
        try:
            headers = {"Authorization": self.pexels_api_key}
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
            
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data.get("photos"):
                photo_url = data["photos"][0]["src"]["large"]
                
                # Download image
                image_response = requests.get(photo_url)
                image_path = os.path.join(temp_dir, filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_response.content)
                
                return image_path
            else:
                raise ValueError("No images found")
                
        except Exception as e:
            raise e
    
    async def _create_placeholder_image(self, temp_dir: str, filename: str) -> str:
        """
        Create a placeholder image when stock images fail
        """
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple colored rectangle
        img = Image.new('RGB', (1920, 1080), color='#2C3E50')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = "Restaurant Scene"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        image_path = os.path.join(temp_dir, filename)
        img.save(image_path)
        
        return image_path
    
    async def _assemble_video(self, audio_path: str, image_paths: List[str], 
                            scenes: List[Dict], temp_dir: str, restaurant_name: str) -> str:
        """
        Assemble final video using ffmpeg
        """
        try:
            self.log_progress("Assembling video")
            
            video_path = os.path.join(temp_dir, f"{restaurant_name}_promo.mp4")
            
            # Calculate scene durations
            total_duration = sum(scene.get("duration", 3) for scene in scenes)
            scene_duration = total_duration / len(scenes) if scenes else 3
            
            # Create video from images
            if image_paths:
                # Use ffmpeg to create video from images and audio
                input_pattern = os.path.join(temp_dir, "scene_%d.jpg")
                
                stream = ffmpeg.input(input_pattern, pattern_type='sequence', framerate=1/scene_duration)
                audio = ffmpeg.input(audio_path)
                
                out = ffmpeg.output(
                    stream, audio, video_path,
                    vcodec='libx264',
                    acodec='aac',
                    shortest=None,
                    pix_fmt='yuv420p'
                )
                
                ffmpeg.run(out, overwrite_output=True)
            else:
                # Create video with just audio
                await self._create_audio_only_video(audio_path, video_path)
            
            return video_path
            
        except Exception as e:
            self.log_progress(f"Video assembly failed: {str(e)}", "error")
            # Create minimal video as fallback
            return await self._create_fallback_video(temp_dir, restaurant_name)
    
    async def _generate_thumbnail(self, video_path: str, temp_dir: str) -> str:
        """
        Generate thumbnail from video
        """
        try:
            thumbnail_path = os.path.join(temp_dir, "thumbnail.jpg")
            
            # Extract frame at 1 second
            stream = ffmpeg.input(video_path, ss=1)
            stream = ffmpeg.output(stream, thumbnail_path, vframes=1)
            ffmpeg.run(stream, overwrite_output=True)
            
            return thumbnail_path
            
        except Exception as e:
            self.log_progress(f"Thumbnail generation failed: {str(e)}", "warning")
            return await self._create_placeholder_image(temp_dir, "thumbnail.jpg")
    
    async def _get_video_metadata(self, video_path: str) -> Dict[str, Any]:
        """
        Get video metadata
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            duration = float(probe['format']['duration'])
            file_size = int(probe['format']['size'])
            resolution = f"{video_info['width']}x{video_info['height']}"
            
            return {
                "duration": duration,
                "file_size": file_size,
                "resolution": resolution
            }
            
        except Exception as e:
            return {
                "duration": 30.0,
                "file_size": 0,
                "resolution": "1920x1080"
            }
    
    async def _generate_silent_audio(self, temp_dir: str, duration: int) -> str:
        """
        Generate silent audio file
        """
        audio_path = os.path.join(temp_dir, "silent.mp3")
        
        # Create silent audio using ffmpeg
        stream = ffmpeg.input('anullsrc=channel_layout=stereo:sample_rate=44100', f='lavfi', t=duration)
        stream = ffmpeg.output(stream, audio_path)
        ffmpeg.run(stream, overwrite_output=True)
        
        return audio_path
    
    async def _create_fallback_video(self, temp_dir: str, restaurant_name: str) -> str:
        """
        Create minimal fallback video
        """
        video_path = os.path.join(temp_dir, f"{restaurant_name}_fallback.mp4")
        
        # Create simple text video
        stream = ffmpeg.input(
            'color=c=blue:size=1920x1080:duration=30', f='lavfi'
        )
        stream = ffmpeg.drawtext(
            stream,
            text=f'{restaurant_name}\\nPromo Video',
            fontcolor='white',
            fontsize=60,
            x='(w-text_w)/2',
            y='(h-text_h)/2'
        )
        stream = ffmpeg.output(stream, video_path)
        ffmpeg.run(stream, overwrite_output=True)
        
        return video_path
    
    async def _create_audio_only_video(self, audio_path: str, output_path: str):
        """
        Create video with just audio and static image
        """
        # Create static image
        stream_video = ffmpeg.input('color=c=black:size=1920x1080', f='lavfi')
        stream_audio = ffmpeg.input(audio_path)
        
        out = ffmpeg.output(
            stream_video, stream_audio, output_path,
            vcodec='libx264',
            acodec='aac',
            shortest=None
        )
        
        ffmpeg.run(out, overwrite_output=True)