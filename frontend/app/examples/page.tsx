import Link from 'next/link'
import { ArrowLeft, Play, Clock, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function ExamplesPage() {
  const examples = [
    {
      id: 1,
      restaurantName: 'Bella Vista Italian',
      style: 'Luxury',
      duration: '30s',
      rating: '4.8',
      thumbnail: '/api/placeholder/400/225',
      description: 'Elegant fine dining experience with authentic Italian cuisine',
      tags: ['Fine Dining', 'Italian', 'Wine Bar']
    },
    {
      id: 2,
      restaurantName: 'Burger Junction',
      style: 'Casual',
      duration: '15s',
      rating: '4.6',
      thumbnail: '/api/placeholder/400/225',
      description: 'Family-friendly burger joint with craft beer selection',
      tags: ['Burgers', 'Casual', 'Family']
    },
    {
      id: 3,
      restaurantName: 'Taco Libre',
      style: 'Street Food',
      duration: '45s',
      rating: '4.9',
      thumbnail: '/api/placeholder/400/225',
      description: 'Authentic Mexican street tacos with fresh ingredients',
      tags: ['Mexican', 'Street Food', 'Authentic']
    },
    {
      id: 4,
      restaurantName: 'The Garden Cafe',
      style: 'Casual',
      duration: '30s',
      rating: '4.7',
      thumbnail: '/api/placeholder/400/225',
      description: 'Fresh, organic cafe with vegan and vegetarian options',
      tags: ['Cafe', 'Vegan', 'Organic']
    },
    {
      id: 5,
      restaurantName: 'Sakura Sushi',
      style: 'Luxury',
      duration: '60s',
      rating: '4.8',
      thumbnail: '/api/placeholder/400/225',
      description: 'Traditional Japanese sushi bar with premium ingredients',
      tags: ['Japanese', 'Sushi', 'Premium']
    },
    {
      id: 6,
      restaurantName: 'Street Noodles',
      style: 'Street Food',
      duration: '20s',
      rating: '4.5',
      thumbnail: '/api/placeholder/400/225',
      description: 'Quick service Asian noodle bowls with bold flavors',
      tags: ['Asian', 'Noodles', 'Quick Service']
    }
  ]

  const getStyleColor = (style: string) => {
    switch (style) {
      case 'Luxury': return 'bg-purple-100 text-purple-700 border-purple-200'
      case 'Casual': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'Street Food': return 'bg-orange-100 text-orange-700 border-orange-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Link>
              </Button>
              <div className="flex items-center gap-2">
                <div className="text-2xl">🎬</div>
                <span className="font-bold text-xl">AI Promo Creator</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
            Video Examples
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            See how AI Promo Creator transforms restaurant listings into engaging promotional videos
          </p>

          <Button size="lg" asChild>
            <Link href="/generate">
              Create Your Video
            </Link>
          </Button>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          <Button variant="outline" className="border-primary text-primary">All Styles</Button>
          <Button variant="ghost">Luxury</Button>
          <Button variant="ghost">Casual</Button>
          <Button variant="ghost">Street Food</Button>
        </div>

        {/* Examples Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {examples.map((example) => (
            <Card key={example.id} className="group hover:shadow-lg transition-shadow duration-300 overflow-hidden">
              <div className="relative">
                {/* Video Thumbnail */}
                <div className="aspect-video bg-muted relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
                    <div className="w-16 h-16 bg-white/80 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform cursor-pointer">
                      <Play className="w-6 h-6 text-primary ml-1" />
                    </div>
                  </div>
                </div>

                {/* Style Badge */}
                <div className="absolute top-3 left-3">
                  <Badge className={getStyleColor(example.style)}>
                    {example.style}
                  </Badge>
                </div>

                {/* Duration Badge */}
                <div className="absolute top-3 right-3">
                  <Badge variant="secondary" className="bg-black/50 text-white border-0">
                    <Clock className="w-3 h-3 mr-1" />
                    {example.duration}
                  </Badge>
                </div>
              </div>

              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-lg">{example.restaurantName}</h3>
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-sm text-muted-foreground ml-1">{example.rating}</span>
                  </div>
                </div>

                <p className="text-muted-foreground text-sm mb-4 line-clamp-2">
                  {example.description}
                </p>

                <div className="flex flex-wrap gap-2">
                  {example.tags.map((tag, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16">
          <h2 className="text-2xl font-bold mb-4">Ready to Create Your Own?</h2>
          <p className="text-muted-foreground mb-6">
            Generate a professional promotional video for your restaurant in just a few minutes
          </p>
          <Button size="lg" asChild>
            <Link href="/generate">
              Get Started Now
            </Link>
          </Button>
        </div>
      </main>
    </div>
  )
}