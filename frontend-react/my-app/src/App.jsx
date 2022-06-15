import React from 'react'
import Home from './components/Home'
import Status from './components/Status'
import GIFS from './components/GIFS'
import {BrowserRouter, Routes, Route} from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/">
            <Route index element={<Home />} />
            <Route path="/gif" element={<GIFS/>}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
     
  )
}

   
export default App    