import React from 'react'

function Home({ isLoggedIn }) {
  return (
    <div className="container mt-4">
      {isLoggedIn ? (
        <h2>Welcome back!</h2>
      ) : (
        <h2>Welcome to SwipeByte</h2>
      )}
    </div>
  )
}

export default Home