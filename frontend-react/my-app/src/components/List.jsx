import React, { useState, useEffect } from "react";
import axios from 'axios'
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList } from 'react-window';


const List = () => {
    const [vidnames, setVidnames] = useState([]);
    var temp2;
    
    const getNames = () =>  { 
        axios.post("http://127.0.0.1/api/list_objs",
            {
                "bucket":"video"
            }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            setVidnames(temp2);
            // console.log("res", res.data);
          })
          .catch(err => {
            console.log("error in request", err);
          });
    }

    useEffect(() => getNames(), [])
    
    function sentRequest(name){
        axios.post("http://127.0.0.1/api/make_gif",
        {
            "filename": name
        }
        ).then(res => {
            console.log(res);
            temp2 = res.data;
            console.log("res", res.data);
            console.log(`sent ${name}`);
          })
          .catch(err => {
            console.log("error in request", err);
          });

        console.log(name);
    }

    function renderRow(props) {
        const { index, style } = props;

        return (
          <ListItem style={style} key={index} component="div" disablePadding>
          <ListItemButton className='button' onClick={() => sentRequest(vidnames[index])}>{vidnames[index]}</ListItemButton>
        </ListItem>
          
        );
      }


    
    return (
        <Box sx={{ width: '100%', height: 299, maxWidth: 360, bgcolor: 'background.paper' }}>
        <FixedSizeList
          height={299}
          width={360}
          itemSize={100}
          itemCount={vidnames.length}
          overscanCount={80}
        >
            {renderRow}
        </FixedSizeList>
      </Box>
    )
}

export default List