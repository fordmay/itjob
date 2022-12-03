score();
side_history();
hide_empty_table();

document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector("#edit_profile_photo")) {
    document.querySelector("#edit_profile_photo").onclick = () => {
      edit_profile_photo();
    }
  }
  if (document.querySelector("#edit_profile_description")) {
    document.querySelector("#edit_profile_description").onclick = () => {
      edit_profile_description();
    }
  }
  if (document.querySelector("#edit_profile_skills")) {
    document.querySelector("#edit_profile_skills").onclick = () => {
      edit_profile_skills();
    }
  }
});

// Check if user is firm
function is_firm() {
  const url_array = window.location.pathname.split("/");
  if (url_array[1] === "firm") {
    return true
  }
  return false
}

function edit_profile_photo() {
  // Show modal and add data there
  document.querySelector("#modal_01").style.display = "block";
  document.querySelector("#example_avatar_pic").src = document.querySelector("#avatar_pic").src;

  if (is_firm()) {
    document.querySelector("#example_firm_name").value = document.querySelector("#firm_name").innerText;
  } else {
    document.querySelector("#example_first_name").value = document.querySelector("#first_name").innerText;
    document.querySelector("#example_last_name").value = document.querySelector("#last_name").innerText;
  }

  document.querySelector("#close_01").onclick = () => {
    // Hide modal and message
    document.querySelector("#modal_01").style.display = "none";
    document.querySelector("#info_message_01").style.display = "none";
    // Clear an HTML image input
    document.querySelector("#input_pic").value = "";

  }
  // Preview an image before it is uploaded
  document.querySelector("#input_pic").onchange = () => {
    const [file] = document.querySelector("#input_pic").files;
    if (file) {
      document.querySelector("#example_avatar_pic").src = URL.createObjectURL(file);
    }
  }
  document.querySelector("#save_01").onclick = () => {
    const form_data = new FormData();
    const fileField = document.querySelector("#input_pic");
    if (fileField.files.length > 0 ? fileField.files[0].size > 1024000 : false) {
      document.querySelector("#info_message_01").style.display = "block";
      document.querySelector("#info_message_01").innerHTML = "image have to be lover 1MB";
    } else {
      form_data.append("avatar", fileField.files[0]);
      if (is_firm()) {
        form_data.append("firm_name", document.querySelector("#example_firm_name").value);
      } else {
        form_data.append("first_name", document.querySelector("#example_first_name").value);
        form_data.append("last_name", document.querySelector("#example_last_name").value);
      }

      fetch("/profile/save_photo", {
        method: "POST",
        body: form_data
      }).then(result => {
        if (result.ok) {
          document.querySelector("#modal_01").style.display = "none";
          document.querySelector("#info_message_01").style.display = "none";
          document.querySelector("#input_pic").value = "";
          document.querySelector("#avatar_pic").src = document.querySelector("#example_avatar_pic").src;
          if (is_firm()) {
            document.querySelector("#firm_name").innerText = document.querySelector("#example_firm_name").value;
          } else {
            document.querySelector("#first_name").innerText = document.querySelector("#example_first_name").value;
            document.querySelector("#last_name").innerText = document.querySelector("#example_last_name").value;
          }
        }
      }).catch(error => {
        console.log("Error:", error);
      });
    }
  }
}

function edit_profile_description() {
  document.querySelector("#modal_02").style.display = "block";
  tinymce.get('textarea').setContent(document.querySelector("#description_value").innerHTML);
  document.querySelector("#close_02").onclick = () => {
    document.querySelector("#modal_02").style.display = "none";
    document.querySelector("#info_message_02").style.display = "none";
  }
  document.querySelector("#save_02").onclick = () => {
    const data = tinymce.get('textarea').getContent();
    if (data.length > 2000) {
      document.querySelector("#info_message_02").style.display = "block";
      document.querySelector("#info_message_02").innerHTML = `${data.length}/2000`;
    } else {
      fetch("/profile/save_description", {
        method: "POST",
        body: JSON.stringify(data)
      }).then(result => {
        if (result.ok) {
          document.querySelector("#modal_02").style.display = "none";
          document.querySelector("#info_message_02").style.display = "none";
          document.querySelector("#description_value").innerHTML = data;
        }
      }).catch(error => {
        console.log("Error:", error);
      });
    }
  }
}


function edit_profile_skills() {
  document.querySelector("#modal_03").style.display = "block";
  const main_table = document.querySelector(".main-table tbody");
  const example_table = document.querySelector(".example-table tbody");

  // Move skills and scores from table_skills to example_table_skills
  const all_skills = document.querySelectorAll(".skill");
  const all_scores = document.querySelectorAll(".score");
  example_table.innerHTML = ""; //clean example_table_skills
  for (let i = 0; i < all_skills.length; i++) {
    example_table.append(create_example_table_skills_row(
      all_skills[i].innerHTML,
      // convert stars to number
      all_scores[i].innerHTML.match(/checked/g) === null ? 0 : all_scores[i].innerHTML.match(/checked/g).length
    ));
  }

  // Add button "+" to the end of example_table_skills
  const add_skill_cell = document.createElement("td");
  add_skill_cell.className = "skill_add";
  add_skill_cell.colSpan = "3";
  const add_skill_div = document.createElement("div");
  add_skill_div.className = "d-grid gap-2";
  const add_skill_button = document.createElement("button");
  add_skill_button.className = "btn btn-dark";
  add_skill_button.type = "submit";
  add_skill_button.innerHTML = "<strong>+</strong>";
  add_skill_button.addEventListener('click', () => {
    // Action to add_skill_button
    example_table.insertBefore(
      create_example_table_skills_row(),
      // add new row before button "+"
      example_table.children[example_table.children.length - 1]
    )
  });
  add_skill_div.append(add_skill_button);
  add_skill_cell.append(add_skill_div);
  example_table.append(add_skill_cell);

  document.querySelector("#close_03").onclick = () => {
    document.querySelector("#modal_03").style.display = "none";
  }

  document.querySelector("#save_03").onclick = () => {
    // Create data with Skills and Scores
    const example_skills = document.querySelectorAll(".example_skill input");
    const example_scores = document.querySelectorAll(".example_score select");
    let data = [];
    for (let i = 0; i < example_skills.length; i++) {
      if (example_skills[i].value !== "") {
        data.push({
          "skill": example_skills[i].value,
          "score": example_scores[i].value
        });
      }
    }

    fetch("/profile/save_skills", {
      method: "POST",
      body: JSON.stringify(data)
    }).then(result => {
      if (result.ok) {
        document.querySelector("#modal_03").style.display = "none";
        main_table.parentElement.parentElement.style.display = "block";
        main_table.innerHTML = "";
        for (let i = 0; i < data.length; i++) {
          main_table.append(create_table_skills_row(data[i].skill, data[i].score));
        }
        score();
        // Hide table if user don't have skills
        if (data.length === 0) {
          main_table.parentElement.parentElement.style.display = "none";
        }
      }
    }).catch(error => {
      console.log("Error:", error);
    });
  }
}

function create_table_skills_row(skill_name, score) {
  const new_row = document.createElement("tr");
  const skill_cell = document.createElement("td");
  skill_cell.className = "skill";
  skill_cell.innerHTML = skill_name;
  new_row.append(skill_cell);
  const score_cell = document.createElement("td");
  score_cell.className = "score";
  score_cell.innerHTML = score;
  new_row.append(score_cell);
  return new_row;
}

function create_example_table_skills_row(skill_name = "", score = 0) {
  const new_row = document.createElement("tr");
  const skill_cell = document.createElement("td");
  skill_cell.className = "example_skill";
  skill_cell.innerHTML = `<input class="form-control" type="text" placeholder="Enter Skill" value="${skill_name}">`;
  new_row.append(skill_cell);
  const score_cell = document.createElement("td");
  score_cell.className = "example_score";
  const select = document.createElement("select");
  select.className = "form-select";
  for (let i = 0; i < 6; i++) {
    const option = document.createElement("option");
    option.value = i;
    option.innerHTML = i;
    if (i === +score) {
      option.defaultSelected = true
    }
    select.append(option);
  }
  score_cell.append(select);
  new_row.append(score_cell);
  const remove_skill_cell = document.createElement("td");
  remove_skill_cell.className = "skill_remove";
  const remove_skill_div = document.createElement("div");
  remove_skill_div.className = "d-grid gap-2";
  const remove_skill_button = document.createElement("button");
  remove_skill_button.className = "btn btn-dark";
  remove_skill_button.type = "submit";
  remove_skill_button.innerHTML = "<strong>-</strong>";
  remove_skill_button.addEventListener('click', () => {
    // Action to remove_skill_button
    remove_skill_button.parentElement.parentElement.parentElement.remove();
  });
  remove_skill_div.append(remove_skill_button);
  remove_skill_cell.append(remove_skill_div);
  new_row.append(remove_skill_cell);
  return new_row;
}

function score() {
  const score = document.querySelectorAll(".score");
  for (let i = 0; i < score.length; i++) {
    score[i].innerHTML = number_to_stars(score[i].innerHTML);
  }
}

function number_to_stars(number) {
  let stars_score = "";
  for (let i = 1; i <= 5; i++) {
    if (i <= number) {
      stars_score = stars_score + "<span class='fa fa-star checked'></span>";
    } else {
      stars_score = stars_score + "<span class='fa fa-star'></span>";
    }
  }
  return stars_score;
}

function hide_empty_table() {
  const main_table = document.querySelectorAll(".main-table tbody");
  for(let i=0; i<main_table.length;i++){
    if(main_table[i].innerHTML.trim() === ""){
      main_table[i].parentElement.parentElement.style.display = "none"
    }
  }
}

function side_history() {
  const container_history = document.querySelectorAll(".container-history");
  for (let i = 0; i < container_history.length; i++) {
    if (i % 2 === 0) {
      container_history[i].classList.add("right");
    } else {
      container_history[i].classList.add("left");
    }
  }
}