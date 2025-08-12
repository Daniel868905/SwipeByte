import React, { useState } from 'react'

function Group({ token }) {
  const [groupName, setGroupName] = useState('')
  const [usernames, setUsernames] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const members = usernames
      .split(',')
      .map((u) => u.trim())
      .filter(Boolean)
    try {
      const res = await fetch('https://localhost:8000/api/v1/groups/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
      
      },
        body: JSON.stringify({ group_name: groupName, members }),
      })
      const data = await res.json()
      if (!res.ok) {
        setMessage(data.error || 'Failed to create group')
      } else {
        setMessage('Group created')
        setGroupName('')
        setUsernames('')
      }
    } catch (e) {
      console.error(e)
      setMessage('Error creating group')
    }
  }

  return (
    <div className="container py-5">
      <h2>Create Group</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Group Name</label>
          <input
            type="text"
            className="form-control"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Usernames (comma separated)</label>
          <input
            type="text"
            className="form-control"
            value={usernames}
            onChange={(e) => setUsernames(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Create
        </button>
      </form>
      {message && <p className="mt-3">{message}</p>}
    </div>
  )
}

export default Group
