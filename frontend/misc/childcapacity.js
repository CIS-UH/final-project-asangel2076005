const fetchPromise = fetch("http://127.0.0.1:5000/api/capacity");


const findRoom = document.querySelector("#findRoom");
const findCapacity = document.querySelector("#findCapacity");
const findChildAmt = document.querySelector("#findChildAmt");
const findSeatsRemain = document.querySelector("#findSeatsRemain");
const clickRoomInfo = document.querySelector("#clickRoomInfo");

fetchPromise
.then((response) => {
    if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();
})
.then((data) => {

    clickRoomInfo.addEventListener("click", () => {
        for (let instance of data) {
            if (findRoom.value == instance["CLASS_ID"]) {
                userCapacity = instance["CLASS_CAPACITY"];
                userChildAmt = instance["CHILD_AMT"];
                userSeatsRemain = instance["SEATS_REMAINING"];
                break;
            }
        }
    
        findCapacity.value = userCapacity;
        findChildAmt.value = userChildAmt;
        findSeatsRemain.value = userSeatsRemain;

    });

})
.catch((error) => {
    console.log(`Could not get data: ${error}`);

    findCapacity.value = error;
    findChildAmt.value = error;
    findSeatsRemain.value = error;
});

// Purpose: User ease of information knowledge about each room's capacity