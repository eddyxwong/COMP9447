import React from 'react'
import Img from "../assets/python.png"
import UploadFileIcon from '@mui/icons-material/UploadFile';

function InputInstructions() {
  return (
    <div className='InputInstructions'>
        <div className='InputInstructionsLogo'>
            <img src={Img} height="100"/>
        </div>
            Drop a Boto3 File here
            <br/>
            or
            <br/>
            <UploadFileIcon/>
            Open from file 
    </div>

  )
}

export default InputInstructions