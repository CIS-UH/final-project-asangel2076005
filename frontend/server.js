// load the things we need
const express = require('express');
const app = express();
const bodyParser  = require('body-parser');
const path = require("path");

// required module to make calls to a REST API
const axios = require('axios');
app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');
app.set("views", path.resolve(__dirname, "views")); 

// Allow script and css to be used by the pages
app.use(express.static(path.join(__dirname, "misc")));

// Begin code here

// Home/Login Route
app.get("/", (req, res) => {

    res.render("pages/index");

});

// Process Login; Hardcoded for now
app.post("/process_login", (req, res) => {

    const username = req.body.username;
    const password = req.body.password;
    let login;

    if (username === "admin" && password === "password") {
        login = "y";
    } else {
        login = "n"
    }

    if (login === "y") {
        res.redirect("/dashboard");
    } else {
        res.render("pages/error", {login});
    }

});

app.get("/dashboard", (req, res) => {
    res.render("pages/dashboard");
});

/*app.post("/process_crud", (req, res) => {

    const crud = req.body.crud;
    const entity = req.body.entity;

    console.log(`${crud} ${entity}`);
});*/


// Facility Webpage
app.get("/facility", (req, res) => {

    axios.get(`http://127.0.0.1:5000/api/facility`)
    .then(response => {
        
        let facility = response.data;
        console.log(facility);
        res.render('pages/entities/facility', {facility});

    })
    .catch(error => {

        let facilityError = "Error fetching facility data from API"

        res.render("pages/error", {
            facilityError
        });

    });
    
});

// Add facility
app.post("/add_facility", (req, res) => {

    const addFacility = req.body;
    console.log(addFacility);

    //Making a POST request to facility API
    axios.post('http://127.0.0.1:5000/api/facility', addFacility)
        .then(response => {
            const addFacilityStatement = response.data
            
            if (addFacilityStatement === "Facility Addition Success") {
                res.redirect("/facility");
            } else {
                res.render("pages/error", {
                    addFacility, 
                    addFacilityStatement,
                    facilityAddError: "Y"
                });
            }
        });
});

// Update facility
app.post("/update_facility", (req, res) => {
    let userFacility = req.body;
    console.log(userFacility);

    axios.get(`http://127.0.0.1:5000/api/facility`)
    .then(response => {
        let facility = response.data;
        let facilityId;

        for (instance of facility) {
            if (userFacility["FACILITY_NAME"].toUpperCase() === instance["FACILITY_NAME"].toUpperCase()) {
                facilityId = instance["FACILITY_ID"];
                break;
            }
        }

        if (facilityId) { // Check if facilityId is set (i.e., a match is found)
            axios.put(`http://127.0.0.1:5000/api/facility/${facilityId}`, userFacility)
            .then(response => {
                const updateFacilityStatement = response.data;
                if (updateFacilityStatement === "Update success") {
                    res.redirect("/facility");
                } else {
                    res.render("pages/error", {
                        userFacility,
                        updateFacilityStatement,
                        facilityUpdateError: "Y"
                    });
                }
            });
        } else {
            // Render error page if no match is found
            const updateFacilityError = "No Matches";
            res.render("pages/error", { updateFacilityError });
        }
    });
});

// Delete facility
app.post("/delete_facility", (req, res) => {
    let userFacility = req.body;
    console.log(userFacility);

    axios.get(`http://127.0.0.1:5000/api/facility`)
    .then(response => {
        let facility = response.data;
        let facilityId;

        for (instance of facility) {
            if (userFacility["FACILITY_NAME"].toUpperCase() === instance["FACILITY_NAME"].toUpperCase()) {
                facilityId = instance["FACILITY_ID"];
                break;
            }
        }

        if (facilityId) { // Check if facilityId is set (i.e., a match is found)
            axios.delete(`http://127.0.0.1:5000/api/facility/${facilityId}`, userFacility)
            .then(response => {
                const deleteFacilityStatement = response.data;
                if (deleteFacilityStatement == `Delete Success`) {
                    res.redirect("/facility");
                } else {
                    res.render("pages/error", {
                        userFacility,
                        deleteFacilityStatement,
                        facilityDeleteError: "Y"
                    });
                }
            });
        } else {
            // Render error page if no match is found
            const deleteFacilityError = "No Matches";
            res.render("pages/error", { deleteFacilityError });
        }
    });
});

// Start the express application on port 8080 and print server start message
const port = 8080;
app.listen(port, () => console.log("Application started and listening on port 8080"));