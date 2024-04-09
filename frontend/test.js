// Delete Teacher
app.post("/delete_teacher", (req, res) => {

    const choice = req.body["choice"];
    console.log(choice);

    axios.delete(`http://127.0.0.1:5000/api/teacher/${choice}`)
    .then(response => {
        const deleteTeacherStatement = response.data;

        if (deleteTeacherStatement == `Delete Teacher Success`) {
            res.redirect("/teacher");
        } else {
            res.render("pages/error", {
                userTeacher,
                deleteTeacherStatement,
                teacherDeleteError: "Y"
            });
        }
    
    })
    .catch(error => {
        res.render("pages/error", {
            deleteTeacherError: "Cannot delete teacher: Referenced by other entities in other table"
        });
    });

});