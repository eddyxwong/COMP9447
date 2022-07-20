import React from 'react'

import PreviousSessions from '../components/PreviousSessions'

// Sessions is a list of all previous comparrisons you have done. A 'session' includes the name of the session, how long ago you accessed it
// and finally a settings cog that lets you choose if it is private, change the name and invite other users to look at it. Aswell as delete it
// New Session button opens a new session a new session is defined as such,

//            NEW ANALYSIS SESSION
//     Upload a new boto3 policy and a policy you want to check it against
//
//      Choose New Policy File      Choose Policy Files to compare
//
//      Session Name*
//      [] private 
//      
//      *Once Both Files are Inputed* CONTINUE

function Sessions() {
    const prevsessions = [
        {id: 1, sessionName:"session1", date:"seconds ago"},
        {id: 2, sessionName:"myfavBoto3", date:"1 week ago"},
        {id: 3, sessionName:"ahahaha", date: "3 weeks ago"},
        {id: 4, sessionName:"WhichPolicyIsThis?", date: "9 months ago"}
    
    ]
  
    return (
    <div className='Sessions'>
        <div className='SessionBox'>
            <button>New Session</button>
            <PreviousSessions data={prevsessions}/>
        </div>
    </div>
  )
}

export default Sessions