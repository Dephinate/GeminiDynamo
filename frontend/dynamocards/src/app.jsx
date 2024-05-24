import React, {useState} from 'react';
import axios from 'axios';
import "./app.css"

function App() {
    const [youtube_link, setYoutubeLink] = useState("");
    const [responseData, setResponseData] = useState(null);

    const handleLinkChange = (event) => {
        console.log(event.target.value)
        setYoutubeLink(event.target.value)
    }

    const sendLink  =  async () => {
        try {
            const response = await axios.post("http://localhost:8000/analyze_video", {
                youtube_link : youtube_link
            });
            setResponseData(response.data)
        } catch (error) {
            console.log(error)
        }

    };

    return (
        <div className="App">
            <h1> Youtube Link to Flashcards Generator</h1>
            <input
                type = "text"
                placeholder = "Paste Youtube Link Here"
                value = {youtube_link}
                onChange = {handleLinkChange}
            />
            <button onClick={sendLink}>
                Generate Flashcards
            </button>
            {responseData && (
                <div>
                    <h2> Response Data: </h2>
                        <p>{JSON.stringify(responseData, null, 2)}</p>
                </div>
            )
            }

        </div>
    )

}

export default App;

// import { useState } from 'preact/hooks'
// import preactLogo from './assets/preact.svg'
// import viteLogo from '/vite.svg'
// import './app.css'

// export function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vitejs.dev" target="_blank">
//           <img src={viteLogo} class="logo" alt="Vite logo" />
//         </a>
//         <a href="https://preactjs.com" target="_blank">
//           <img src={preactLogo} class="logo preact" alt="Preact logo" />
//         </a>
//       </div>
//       <h1>Vite + Preact</h1>
//       <div class="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/app.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p class="read-the-docs">
//         Click on the Vite and Preact logos to learn more
//       </p>
//     </>
//   )
// }

