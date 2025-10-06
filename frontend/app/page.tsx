import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ArrowRight, MapPin, Bot, Download, Clock, Star, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="text-2xl">🎬</div>
              <span className="font-bold text-xl">AI Promo Creator</span>
            </div>
            <div className="flex items-center space-x-6">
              <Link href="/pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </Link>
              <Link href="/examples" className="text-muted-foreground hover:text-foreground transition-colors">
                Examples
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="text-center max-w-4xl mx-auto">
          <div className="flex justify-center mb-6">
            <Badge variant="secondary" className="text-sm px-3 py-1">
              <Zap className="w-3 h-3 mr-1" />
              AI-Powered Video Generation
            </Badge>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
            Generate Restaurant Videos
            <br />
            <span className="text-primary">in Minutes</span>
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
            Turn any Google Maps restaurant link into a professional promotional video. 
            AI-powered script generation, voiceover, and video assembly.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button asChild size="lg" className="text-base px-8">
              <Link href="/generate">
                Start Creating 
                <ArrowRight className="ml-2 w-4 h-4" />
              </Link>
            </Button>
            
            <Button variant="outline" size="lg" className="text-base px-8">
              <Link href="/examples">
                View Examples
              </Link>
            </Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary mb-1">
                <Clock className="w-5 h-5 inline mr-1" />
                3 min
              </div>
              <p className="text-sm text-muted-foreground">Average generation time</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary mb-1">
                <Star className="w-5 h-5 inline mr-1" />
                4.9/5
              </div>
              <p className="text-sm text-muted-foreground">User satisfaction</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-primary mb-1">
                <Bot className="w-5 h-5 inline mr-1" />
                90%+
              </div>
              <p className="text-sm text-muted-foreground">Success rate</p>
            </div>
          </div>
        </div>

        <Separator className="my-16" />

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPin className="w-8 h-8 text-primary" />
              </div>
              <CardTitle className="text-xl">Paste URL</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base leading-relaxed">
                Simply paste a Google Maps restaurant URL and let AI do the rest
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Bot className="w-8 h-8 text-primary" />
              </div>
              <CardTitle className="text-xl">AI Generation</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base leading-relaxed">
                Advanced AI extracts menu, writes script, and creates professional video
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
            <CardHeader>
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Download className="w-8 h-8 text-primary" />
              </div>
              <CardTitle className="text-xl">Download & Share</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base leading-relaxed">
                Get your MP4 file ready to share on social media in under 3 minutes
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}