import './sidebar.scss'
import { useNavigate } from "react-router-dom";
import DashboardIcon from '@mui/icons-material/Dashboard';
import PreviewIcon from '@mui/icons-material/Preview';

const Sidebar = () => {

    let navigate = useNavigate(); 
    const routeChange_gif = () =>{ 
      let path = `/gif`; 
      navigate(path);
    }

    const routeChange_home = () =>{ 
        let path = `/`; 
        navigate(path);
      }

    return (
        <div className='sidebar'>
            <div className='top'>
                <DashboardIcon className='icon' onClick={routeChange_home}/>
                <span className='logo' onClick={routeChange_home}>Video Thumbnailer</span>
            </div>
            <hr></hr>
            <div className='center'>
                <ul>
                    <li>
                        <PreviewIcon className='icon' onClick={routeChange_gif}/>
                        <span onClick={routeChange_gif}>View Gif</span>
                    </li>
                </ul>
            </div>
        </div>

    )

}

export default Sidebar