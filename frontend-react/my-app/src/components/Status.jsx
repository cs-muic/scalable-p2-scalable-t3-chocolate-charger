import React, { useState, useEffect } from "react";
import axios from 'axios'
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList } from 'react-window';


const Status = () => {
    const [status, setStatus] = useState([]);

    var temp3;
    
    const getStatus = () =>  { 
        axios.get("http://127.0.0.1/api/get_status"
        ).then(res => {
            console.log(res);
            temp3 = res.data;
            console.log(temp3)
            setStatus(temp3);
            // console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getStatus(), [])
    
    function renderRow(props) {
        const { index, style } = props;

        return (
          // <ListItem style={style} key={index} component="div" disablePadding>
          //   {/* {status.map((sta) => <ListItemText>{sta}</ListItemText>)} */}
          //   <ListItemText primary={`Item ${index + 1}`} />
          // </ListItem>
          <ListItem style={style} key={index} component="div" disablePadding>
          <ListItemText>{status[index]}</ListItemText>
        </ListItem>
          
        );
      }


    return (
        // <div>
        //     {status.map((sta) => <h1>{sta}</h1>)}
        // </div>
        <Box sx={{ width: '100%', height: 299, maxWidth: 360, bgcolor: 'background.paper' }}>
      <FixedSizeList
        height={299}
        width={360}
        itemSize={100}
        itemCount={status.length}
        overscanCount={100}
      >
        {renderRow}
      </FixedSizeList>
    </Box>
    )
}

export default Status