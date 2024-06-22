console.log("Hello from external blogs_web/index.html");
$(document).ready(function () {
  let editBlogId;
  const blogsUrl = document
    .getElementById("blogs-blogs")
    .getAttribute("data-url");
  const blogWithIdZero = document
    .getElementById("blogs-blog")
    .getAttribute("data-url");
  console.log("blogsUrl:", blogsUrl);
  console.log("blogWithIdZero:", blogWithIdZero);

  // Function to fetch blogs
  function fetchBlogs() {
    $.ajax({
      url: blogsUrl,
      method: "GET",
      headers: {
        Authorization: localStorage.getItem("access_token"),
        Accept: "application/json",
      },
      success: function (data) {
        $("#blogList").empty();
        data.forEach(function (blog) {
          $("#blogList").append(`
                                <li class="list-group-item" data-id="${
                                  blog.id
                                }">
                                    <a href="#" class="blog-link">${
                                      blog.title
                                    }</a>
                                    <p>${
                                      blog.content.length > 200
                                        ? blog.content.substring(0, 200) + "..."
                                        : blog.content
                                    }</p>
                                </li>
                            `);
        });
      },
    });
  }

  // Fetch blogs on page load
  fetchBlogs();

  // Handle form submission for creating a blog
  $("#blogForm").on("submit", function (e) {
    e.preventDefault();
    const title = $("#title").val();
    const content = $("#content").val();

    $.ajax({
      url: blogsUrl,
      method: "POST",
      contentType: "application/json",
      headers: {
        Authorization: localStorage.getItem("access_token"),
        Accept: "application/json",
      },
      data: JSON.stringify({ title: title, content: content }),
      success: function () {
        // Clear form
        $("#title").val("");
        $("#content").val("");
        // Refresh blog list
        fetchBlogs();
      },
    });
  });

  // Handle click on blog item for editing
  $("#blogList").on("click", ".list-group-item", function () {
    editBlogId = $(this).data("id");
    const title = $(this).find(".blog-link").text();
    const content = $(this).find("p").text();

    $("#editTitle").val(title);
    $("#editContent").val(content);
    $("#editBlogModal").modal("show");
  });

  // Handle form submission for editing a blog
  $("#editBlogForm").on("submit", function (e) {
    e.preventDefault();
    const title = $("#editTitle").val();
    const content = $("#editContent").val();
    var blogUrl = `${blogWithIdZero}`.slice(0, -1); // Remove the trailing '0' to get the base URL

    $.ajax({
      url: `${blogUrl}${editBlogId}`,
      method: "PUT",
      contentType: "application/json",
      headers: {
        Authorization: localStorage.getItem("access_token"),
        Accept: "application/json",
      },
      data: JSON.stringify({ title: title, content: content }),
      success: function () {
        $("#editBlogModal").modal("hide");
        fetchBlogs();
      },
    });
  });
});
