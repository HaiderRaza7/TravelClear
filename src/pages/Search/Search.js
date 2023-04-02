import React from "react";
import styles from "./Search.scss";

const Search = () => {
    // let searchBtn = (e) => {
    //     e.preventDefault();  
    // };
    return(
        <form
        className={`${styles.search} d-flex flex-sm-row flex-column align-items-center justify-content-center gap-4 mb-5`}
        >
            <input
            // onChange = {(e) = {
            //     //data search with python
            // }}
            placeholder = "Search for location"
            className = {styles.input}
            type = "text"
            />
            <button
             className={`${styles.btn} btn btn-primary fs-5`}
            >
                Search
            </button>

        </form>
    );
};

export default Search;