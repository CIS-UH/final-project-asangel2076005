const fetchPromise = fetch("http://127.0.0.1:5000/api/space");
// Calls this extra api to provide users with more information about teacher capacity in each rooms

// DOM calls on teacher webpage 
const findRoom = document.querySelector("#findRoom");
const findSpaces = document.querySelector("#findSpaces");
const findTeacherAmt = document.querySelector("#findTeacherAmt");
const findSpaceRemain = document.querySelector("#findSpaceRemain");
const clickSpaceInfo = document.querySelector("#clickSpaceInfo");

fetchPromise
.then((response) => {
    if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();

    // If API is not running, throw this basic webpage

})
.then((data) => {

    clickSpaceInfo.addEventListener("click", () => {
        for (let instance of data) {
            if (findRoom.value == instance["CLASS_ID"]) {
                userSpace = instance["ROUNDED_CAPACITY"];
                userTeacherAmt = instance["TEACHER_AMT"];
                userSpaceRemain = instance["SPACE_REMAINING"];
                break;
            }
        }
    
        findSpaces.value = userSpace;
        findTeacherAmt.value = userTeacherAmt;
        findSpaceRemain.value = userSpaceRemain;

    });

})
.catch((error) => {
    console.log(`Could not get data: ${error}`);

    findSpaces.value = error;
    findTeacherAmt.value = error;
    findSpaceRemain.value = error;

    // Throw the same errors on all 3 inputs if CORS blocks the API call
});

// Purpose: User ease of information knowledge about each room's capacity