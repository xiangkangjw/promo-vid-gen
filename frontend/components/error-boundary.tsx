'use client'

import { Component, ReactNode } from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
  errorInfo: any
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)

    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('Error caught by boundary:', error, errorInfo)

    this.setState({
      error,
      errorInfo,
    })

    // Report error to monitoring service
    if (process.env.NODE_ENV === 'production') {
      // Here you would send to your error reporting service
      // Example: Sentry.captureException(error)
    }
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    })
  }

  handleReload = () => {
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20 flex items-center justify-center p-4">
          <Card className="w-full max-w-md">
            <CardHeader className="text-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
              <CardTitle className="text-xl">Something went wrong</CardTitle>
              <CardDescription>
                We're sorry, but something unexpected happened. Please try again.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <p className="text-sm font-medium text-red-800 mb-2">Error Details:</p>
                  <p className="text-xs text-red-700 font-mono whitespace-pre-wrap">
                    {this.state.error.toString()}
                  </p>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-2">
                <Button onClick={this.handleReset} variant="outline" className="flex-1">
                  Try Again
                </Button>
                <Button onClick={this.handleReload} className="flex-1">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Reload Page
                </Button>
              </div>

              <p className="text-xs text-muted-foreground text-center">
                If this problem persists, please contact support.
              </p>
            </CardContent>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

// Hook version for functional components
export function useErrorHandler() {
  return (error: Error, errorInfo?: any) => {
    console.error('Error handled:', error, errorInfo)

    if (process.env.NODE_ENV === 'production') {
      // Report to error monitoring service
      // Example: Sentry.captureException(error)
    }
  }
}