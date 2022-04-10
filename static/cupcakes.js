
const base_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
    <div id="${cupcake.id}">
      <li>
       Flavor: ${cupcake.flavor} / Size: ${cupcake.size} / Rating :${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="img"
      src="${cupcake.image}">
    </div>
  `;
}


async function showCupcakes() {
    const res = await axios.get(`${base_URL}/cupcakes`);
    for (let cupcake of res.data.cupcakes) {
        let newCupcake = generateCupcakeHTML(cupcake);
        $("#cupcakes-list").append(newCupcake);
    }
}


$("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();


    const newCupcakeRes = await axios.post(`${base_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeRes.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$("#cupcakes-list").on("click", ".delete-button", async function (e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("id");

    await axios.delete(`${base_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


showCupcakes();