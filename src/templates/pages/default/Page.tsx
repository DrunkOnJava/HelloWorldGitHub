import React from "react"
import "./Page.css"

interface PageProps {
  // Add page props here
}

export const Page: React.FC<PageProps> = (props) => {
  return (
    <div className="page">
      <header className="page-header">
        <h1>Page Title</h1>
      </header>
      <main className="page-content">
        {/* Add page content here */}
      </main>
    </div>
  )
}

export default Page
