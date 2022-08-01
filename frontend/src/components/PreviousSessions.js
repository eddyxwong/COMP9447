import React from 'react'

// Date will obviously be changed


export default function PreviousSessions({data}) {
    return (
        <div className='PrevSessions'>
          {data.map(({id, sessionName, date}) => {
            return (
              <div key={id}>
                <h2>name: {sessionName}</h2>
                <h2>date  : {date}</h2>
    
                <hr />
              </div>
            );
          })}
        </div>
      );
    }

