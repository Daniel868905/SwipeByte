import React, { useCallback, useEffect, useState } from 'react'
import { API_BASE_URL } from '../config'

function Groups({ token }) {
  const [groups, setGroups] = useState([])
  const [newMembers, setNewMembers] = useState({})

  const fetchGroups = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/groups/`, {
        headers: { Authorization: `Token ${token}` },
      })
      const data = await res.json()
      if (res.ok) {
        setGroups(data)
      }
    } catch (e) {
      console.error(e)
    }
  }, [token])

  useEffect(() => {
    fetchGroups()
  }, [fetchGroups])


   const handleAdd = async (groupId) => {
    const members = (newMembers[groupId] || '')
      .split(',')
      .map((m) => m.trim())
      .filter(Boolean)
    if (!members.length) return
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/groups/${groupId}/members/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({ members }),
        },
      )
      if (res.ok) {
        setNewMembers({ ...newMembers, [groupId]: '' })
        fetchGroups()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const handleRemove = async (groupId, email) => {
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/v1/groups/${groupId}/members/`,
        {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({ members: [email] }),
        },
      )
      if (res.ok) {
        fetchGroups()
      }
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="container py-5">
      <h2>Your Groups</h2>
      {groups.map((group) => (
        <div key={group.id} className="mb-4">
          <h4>{group.group_name}</h4>
          <ul>
            {group.members.map((member) => (
              <li key={member.id}>
                {member.email}
                <button
                  className="btn btn-sm btn-danger ms-2"
                  onClick={() => handleRemove(group.id, member.email)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <div className="input-group mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Add member emails"
              value={newMembers[group.id] || ''}
              onChange={(e) =>
                setNewMembers({ ...newMembers, [group.id]: e.target.value })
              }
            />
            <button
              className="btn btn-primary"
              onClick={() => handleAdd(group.id)}
            >
              Add
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

export default Groups