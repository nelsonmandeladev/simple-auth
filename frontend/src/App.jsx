import "bootstrap/dist/css/bootstrap.min.css"
import Home from "./components/Home";
import Dashboard from "./components/Home";
import Layout from "./components/Layout";
import Login from "./components/Login";
import Unauthorized from "./components/Unauthorized"
import Register from "./components/Register";
import RequireAuth from "./components/RequireAuth"
import { Route, Routes } from "react-router-dom";
import NotFound from "./components/NotFound"


const ROLES = {
  'User': 2001,
  'Editor': 1984,
  'Admin': 5150
} 

function App() {

  return (
    <Routes>
      <Route path="/" element = { <Layout /> } >
        <Route path="/register" element = { <Register /> } />
        <Route path="/login" element = { <Login /> } />
        <Route path="/unauthorized" element = { <Unauthorized /> } />
        <Route path="/" element = {<Home />} />
        
        <Route element = {<RequireAuth allowedRoles={[ROLES.User]} />}>
          <Route path="/dashboard" element = {<Dashboard />}/>
        </Route>

        <Route path="*" element = {<NotFound />} />
      </Route>
    </Routes>
  )
}

export default App
