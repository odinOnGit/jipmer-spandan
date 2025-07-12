import React from 'react'
import { Link } from 'react-router'

const HomePage = () => {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h1>Welcome to Spandan Registration</h1>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1rem',
        marginTop: '2rem'
      }}>
        <Link to="/delegate-card" style={{
          padding: '1.5rem',
          border: '1px solid #e5e7eb',
          borderRadius: '0.5rem',
          textDecoration: 'none',
          color: 'inherit',
          transition: 'box-shadow 0.2s',
          ':hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
          }
        }}>
          <h2>🎫 Delegate Card</h2>
          <p>Register for your delegate card</p>
        </Link>
        
        <Link to="/event-register" style={{
          padding: '1.5rem',
          border: '1px solid #e5e7eb',
          borderRadius: '0.5rem',
          textDecoration: 'none',
          color: 'inherit',
          transition: 'box-shadow 0.2s',
          ':hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
          }
        }}>
          <h2>🎟️ Event Registration</h2>
          <p>Register for events</p>
        </Link>
        
        <Link to="/pass-purchase" style={{
          padding: '1.5rem',
          border: '1px solid #e5e7eb',
          borderRadius: '0.5rem',
          textDecoration: 'none',
          color: 'inherit',
          transition: 'box-shadow 0.2s',
          ':hover': {
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
          }
        }}>
          <h2>🏷️ Pass Purchase</h2>
          <p>Buy event passes</p>
        </Link>
      </div>
    </div>
  )
}

export default HomePage