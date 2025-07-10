import React from 'react'
import { Outlet, Link } from 'react-router'
import './Navbar.css'

function Navbar() {
  return (
    <nav id="navbar">
        <img id="logo" alt="spandan logo" src="/assets/spandan_logo.png"></img>
        <ul id="navitems">
            <Link className='navlinks' to='/'><li>Home</li></Link>
            <Link className='navlinks' to='/about'><li>About</li></Link>
            <Link className='navlinks' to='/events'><li>Events</li></Link>
            <Link className='navlinks' to='/register'><li>Register</li></Link>
            <Link className='navlinks' to='/contact'><li>Contact</li></Link>
            
        </ul>
    </nav>
  )
}

export default Navbar