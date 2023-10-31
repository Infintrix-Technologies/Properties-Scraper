import React from 'react'
import { Routes, Route } from "react-router-dom"
import About from './pages/About'
import RightMove from './pages/RightMove'
const Routespath = () => {
    return (
        <>

            <Routes>
                <Route path="/" element={<RightMove />} />
                <Route path="/about" element={<About />} />
            </Routes>
        </>
    )
}

export default Routespath