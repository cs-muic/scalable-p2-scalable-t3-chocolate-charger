import React, { useState, useEffect } from "react";
import axios from 'axios'


const List = () => {
    const [vidnames, setVidnames] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const temp = axios.get("http://127.0.0.1:8081/api/list_objs",
            {
                "bucket":"video"
            }
        )

    console.log(temp)
    // function getvidnames() {
    //     axios.post("http://127.0.0.1:8081/api/list_objs",
    //         {
    //             "bucket":"video"
    //         }
    //     )
    //     .then(response => {
    //         setVidnames(response.data)
    //     });
    // }


    
    return (
            <div>
                {vidnames}
            </div>
    )
}

export default List