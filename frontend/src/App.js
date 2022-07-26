// import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import Dropzone from 'react-dropzone';
import InputInstructions from './components/InputInstructions';
import Diff from './components/Diff';
import logo from './assets/Transparent.png';


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
        <div className="App">
            <img src={logo}/>
            <div className="Description">
               <p>
                    Welcome to IAM Static, your very own IAM policy generator that
                    enforces least privilege!
                    <br></br>
                    Currently we only support python boto3 scripts to generate your IAM
                    policy files but stay tuned!
                    <br></br>
                </p>
            </div>
            <div className="Upload">
                <div className="Left">
                    <h2>New Policy</h2>
                <Dropzone multiple={false} onDrop={acceptedFiles => console.log(acceptedFiles)}>
                    {({getRootProps, getInputProps}) => (
                        <section className='Drop'>
                        <div {...getRootProps()}>
                            <input {...getInputProps()} 
                                hidden
                                accept=".py"
                                multiple
                                type="file"
                                // value={selectedFile}
                                onChange={multiple}
                            />
                            <InputInstructions/>
                        </div>
                        </section>
                )}
                </Dropzone>
                </div>
                
                <div className="Right">
                    <h2>Current Policy</h2>
                <Dropzone multiple={false} onDrop={acceptedFiles => console.log(acceptedFiles)}>
                    {({getRootProps, getInputProps}) => (
                        <section className="Drop">
                        <div {...getRootProps()}>
                            <input {...getInputProps()} 
                                hidden
                                accept=".py"
                                multiple
                                type="file"
                                // value={selectedFile}
                                onChange={multiple}
                            />
                            <InputInstructions/>
                        </div>
                        </section>
                )}
                </Dropzone>
                </div>
            </div>
            <div>
                <Diff/>
            </div>
        </div>
    );
}
