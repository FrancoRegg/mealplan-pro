import { createContext, useState } from 'react'

// eslint-disable-next-line react-refresh/only-export-components
export const MenuContext = createContext()

export const MenuProvider = ({children}) => {

  const[currentMenu, setCurrentMenu] = useState(null)

  const generateMenu = (newMenu) => {
    setCurrentMenu(newMenu)
  }

  const regenerateDay = () => {

  }
  return(
    <MenuContext.Provider value={{currentMenu, generateMenu, regenerateDay}}>
      {children}    
    </MenuContext.Provider>
  )
}