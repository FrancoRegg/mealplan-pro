import { createContext, useState } from 'react'

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  
  const [user, setUser] = useState("")
  const [token, setToken] = useState("")
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  
  const login = (token, userData) => {
    setUser(userData)
    setToken(token)
    setIsAuthenticated(true)
  }
  const logout = () => {
    setUser("")
    setToken("")
    setIsAuthenticated(false)
  }

  return (
  <AuthContext.Provider value={{user, token, isAuthenticated, login, logout}}>
    {children}
  </AuthContext.Provider>
  )
}