const API_URL = "http://localhost:8000/api/v1"

const login = async(email, password) => {

  try{
    const response = await fetch(`${API_URL}/auth/login/`,{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({email, password})
    })
    const data = await response.json()

    return data

  }catch(error){
    console.error("¡Ups! Algo salió mal:", error);
  }
}