import React from 'react'

function Home({ isLoggedIn }) {
  return (
    <div className="container py-5">
      <div className="p-5 mb-4 bg-body-tertiary rounded-3 text-center">
        <h1 className="display-5 fw-bold">
          {isLoggedIn ? 'Welcome back!' : 'Welcome to SwipeByte'}
        </h1>
        {!isLoggedIn && (
          <p className="fs-5">Create an account or log in to start using the app.</p>
        )}
      </div>
    </div>
  )
}

export default Home