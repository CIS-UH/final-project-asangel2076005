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