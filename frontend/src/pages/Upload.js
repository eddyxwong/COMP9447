import React from 'react'

//            NEW ANALYSIS SESSION
//     Upload a new boto3 policy and a policy you want to check it against
//
//      Choose New Policy File      Choose Policy Files to compare
//
//      Session Name*
//      [] private 
//      
//      *Once Both Files are Inputed* CONTINUE

function upload() {
  return (
    <div className='Upload'>
        <h1>New Analysis Session</h1>
        <h6>Upload both a boto3 file and a policy, group of policies or repo / link to begin an analysis session</h6>
        <div className='upload buttons'>
                <button>Upload new Boto3 file</button>
                <button>Upload comparable policies</button>
        </div>
        <div>
            <h3> Session Name </h3>
            <input />
        </div>
        <div>
            <input type="checkbox"/> <h3>private</h3>
        </div>
        <button>continue</button>
    </div>
  )
}

export default upload