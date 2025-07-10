import React, { useState } from 'react'
import './Events.css'

const modules = import.meta.glob('../events/**/**/index.jsx', { eager: true })

function Events() {

    const [category, setCategory] = useState("All");

    const eventCards = Object.entries(modules).map(([path, module]) => {
        const type = path.split('/')[2]
        const name = path.split('/')[3] // mentee folder name
        const meta = module.meta || {}
        return {
        //   title: meta.title || `${name}'s App`,
        //   author: meta.author || name,
        //   description: meta.description || '',
        //   thumbnail: meta.thumbnail || '', // fallback empty

        type,
        name,
        fee: meta.fee,
        thumbnail: meta.thumbnail,
        description: meta.description,
        details: meta.details,
        }
      })
    
      const categories = [...new Set(eventCards.map(d => d.type))];
    //   const eventsByCategory = categories.reduce((acc, cat) => {
    //     acc[cat] = rawData.filter(e => e.category === cat);
    //     return acc;
    //   }, {});

      

  return (
    <>
    <section className="spandan-events-section">
    <div className="spandan-banner">
      <h1>SPANDAN EVENTS</h1>
      <p>
        Unleash your talents across cultural performances, sports championships, fine arts, literary competitions, and creative challenges!
      </p>
      <div className="event-filters">
        {/* <button className="filter active">All</button>
        <button className="filter">Cultural - Major</button>
        <button className="filter">Cultural - Minor</button>
        <button className="filter">Fine Arts</button>
        <button className="filter">Sports</button>
        <button className="filter">Literary</button>
        <button className="filter">Online</button>
        <button className="filter">Photography</button> */}

        <button onClick={() => setCategory("All")}>All</button>
        {categories.map(cat => (
        <button key={cat} onClick={() => setCategory(cat)}>
        {cat}
        </button>
      ))}
        
      </div>
    </div>
    <div className="event-cards-container">
      {(category === "All" ? eventCards : eventCards.filter(e => e.type === category)).map(({ type, name, fee, thumbnail, description, details }) => (
        
        <div className={`event-card major ${name.replaceAll(" ", "-").replace("-", " ").replace("(", "").replace(")", "").toLowerCase()}`}>
        <div id="top"><span className="category-badge">{type}</span>
        <p className="registration-fee">Rs.<b>{fee}</b></p></div>
        <div className="event-photo" background-image={`${thumbnail}`}></div>

        <h2>{name}</h2>
        <p className="subtitle">{description}</p>
        <ul className="event-details">
          <li>{details[0]}</li>
          <li>{details[1]}</li>
          <li>{details[2]}</li>
        </ul>

        </div>

      ))}
    </div></section>
    
    </>
  )
}

export default Events

