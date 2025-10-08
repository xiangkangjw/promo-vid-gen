import Link from 'next/link'
import { ArrowLeft, Check } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function PricingPage() {
  const plans = [
    {
      name: 'Starter',
      price: '$29',
      period: 'per video',
      description: 'Perfect for trying out our service',
      features: [
        '1 promotional video',
        'Up to 30 seconds duration',
        'HD video quality (720p)',
        'Basic style options',
        'Email support'
      ],
      cta: 'Start Creating',
      popular: false
    },
    {
      name: 'Professional',
      price: '$79',
      period: 'per month',
      description: 'Best for small restaurants',
      features: [
        '5 promotional videos per month',
        'Up to 60 seconds duration',
        'Full HD quality (1080p)',
        'All style options',
        'Priority support',
        'Custom branding',
        'Social media formats'
      ],
      cta: 'Go Professional',
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'contact us',
      description: 'For restaurant chains and agencies',
      features: [
        'Unlimited videos',
        'Custom durations',
        '4K video quality',
        'White-label solution',
        'API access',
        'Dedicated support',
        'Custom integrations',
        'Bulk processing'
      ],
      cta: 'Contact Sales',
      popular: false
    }
  ]

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
            Simple, Transparent Pricing
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
            Choose the plan that fits your restaurant's needs. No hidden fees, cancel anytime.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <Card key={index} className={`relative ${plan.popular ? 'border-primary shadow-lg scale-105' : 'border-border'}`}>
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-primary text-primary-foreground px-3 py-1">
                    Most Popular
                  </Badge>
                </div>
              )}

              <CardHeader className="text-center pb-6">
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-muted-foreground ml-2">/{plan.period}</span>
                </div>
                <CardDescription className="mt-2">{plan.description}</CardDescription>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center">
                      <Check className="w-4 h-4 text-primary mr-3 flex-shrink-0" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Button
                  className="w-full"
                  variant={plan.popular ? "default" : "outline"}
                  asChild
                >
                  <Link href="/generate">
                    {plan.cta}
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="mt-24 max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
          <div className="grid gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-2">How long does it take to generate a video?</h3>
              <p className="text-muted-foreground">Most videos are generated within 2-3 minutes. Complex restaurants with extensive menus may take up to 5 minutes.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">What video formats do you support?</h3>
              <p className="text-muted-foreground">We provide MP4 files optimized for social media platforms including Instagram, TikTok, Facebook, and YouTube.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Can I customize the video style?</h3>
              <p className="text-muted-foreground">Yes! We offer three main styles: Luxury, Casual, and Street Food. Professional and Enterprise plans include additional customization options.</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">What if I'm not satisfied with the video?</h3>
              <p className="text-muted-foreground">We offer free regeneration with different styles. If you're still not satisfied, we provide a full refund within 24 hours.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}