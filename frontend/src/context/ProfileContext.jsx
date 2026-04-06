import { createContext, useState } from 'react'

// eslint-disable-next-line react-refresh/only-export-components
export const ProfileContext = createContext()

export const ProfileProvider = ({children}) => {

  const [profile, setProfile] = useState(null)

  const updateProfile = (profile) =>{
    setProfile(profile)
  }

  return(
    <ProfileContext.Provider value={{profile, updateProfile}}>
      {children}
    </ProfileContext.Provider>
  )
}