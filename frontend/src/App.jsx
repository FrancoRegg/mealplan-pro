import { Routes, Route } from 'react-router-dom'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Profile } from './pages/Profile'
import { Ingredients } from './pages/Ingredients'
import { Menu } from './pages/Menu'

import './App.css'

function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<Login />}/>
        <Route path="/register" element={<Register />}/>
        <Route path="/profile" element={<Profile />}/>
        <Route path="/ingredients" element={<Ingredients />}/>
        <Route path="/menu" element={<Menu />}/>
      </Routes>
    </>
  )
}

export default App
