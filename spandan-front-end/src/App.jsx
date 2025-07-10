import Navbar from "./components/Navbar"
import Events from "./pages/Events"
import Home from "./pages/Home"
import { BrowserRouter, Routes, Route } from 'react-router'

function App() {

  return (
    <>
    <BrowserRouter><Navbar />
      <Routes>
        <Route path = '/' element = {<Home />} />
        <Route path = '/events' element = {<Events />} />
        
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
