// import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import Button from '@mui/material/Button';

export default function App() {
    // let multiple = async (e) => {
    //     Array.from(e.target.files).forEach((file) => {
    //         let reader = new FileReader();
    //         reader.onload = () => {
    //             console.log(reader.result);
    //             setMyArray([reader.result]);
    //             console.log(myArray);
    //         };
    //         reader.readAsText(file);
    //         // console.log(reader.readAsText);
    //         // setMyArray((myArray) => [...myArray, reader.result]);
    //         // console.log(myArray);
    //     });
    const multiple = async (e) => {
        // Convert the FileList into an array and iterate
        let files = Array.from(e.target.files).map((file) => {
            // Define a new file reader
            let reader = new FileReader();

            // Create a new promise
            return new Promise((resolve) => {
                // Resolve the promise after reading file
                reader.onload = () => resolve(reader.result);

                // Reade the file as a text
                reader.readAsText(file);
            });
        });

        // At this point you'll have an array of results
        let res = await Promise.all(files);
        console.log(res);
    };

    return (
        <div
            className="App"
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
            }}
        >
            <h1>IAM STATIC</h1>
            Welcome to IAM Static, your very own IAM policy generator that
            enforces least privilege!
            <br></br>
            Currently we only support python boto3 scripts to generate your IAM
            policy files but stay tuned!
            <br></br>
            <Button variant="contained" component="label">
                Upload
                <input
                    hidden
                    accept=".py"
                    multiple
                    type="file"
                    // value={selectedFile}
                    onChange={multiple}
                />
            </Button>
        </div>
    );
}
