// Delete Facility
app.post("/delete_facility", (req, res) => {

    const choice = req.body["choice"];
    console.log(choice);

    axios.delete(`http://127.0.0.1:5000/api/classroom/${choice}`)
    .then(response => {
        const deleteFacilityStatement = response.data;

        if (deleteFacilityStatement == `Classroom Delete Success`) {
            res.redirect("/facility");
        } else {
            res.render("pages/error", {
                userFacility,
                deleteFacilityStatement,
                facilityDeleteError: "Y"
            });
        }
    
    })
    .catch(error => {
        res.render("pages/error", {
            deleteFacilityError: "Cannot delete facility: Referenced by other entities in other table"
        })
    });

});