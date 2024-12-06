/** @type {import('next').NextConfig} */
const nextConfig = {}

module.exports = nextConfig

// next.config.js
module.exports = {
  redirects: async () => {
    return [
      {
        source: '/', // Redirect from the root path
        destination: '/about', // Redirect to the 'about' page
        permanent: true // Use a 308 permanent redirect
      },
      {
        source: '/dashboard', // Redirect from the root path
        destination: '/about', // Redirect to the 'about' page
        permanent: true // Use a 308 permanent redirect
      }
    ]
  }
}