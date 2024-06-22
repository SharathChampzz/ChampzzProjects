console.log("Hello from external blogs_web/index.html");
$(document).ready(function () {
  let editBlogId;
  const blogsUrl = document.getElementById("blogs-blogs").getAttribute("data-url");
  const blogWithIdZero = document.getElementById("blogs-blog").getAttribute("data-url");
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

   // Handle click on blog item for editing
   $("#add-blog").on("click", function () {
    $("#editBlogModalLabel").text('Add Blog');
    $("#editTitle").val("");
      $("#editContent").val("");
    $("#deleteblog").hide();
    $("#editBlogModal").modal("show");
    editBlogId = undefined;
  });

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
    $("#deleteblog").show();
    $("#editBlogModal").modal("show");
  });

  // Handle form submission for editing a blog
  $("#editBlogForm").on("submit", function (e) {
    e.preventDefault();
    console.log("editBlogForm submitted")
    const title = $("#editTitle").val();
    const content = $("#editContent").val();
    var blogUrl = `${blogWithIdZero}`.slice(0, -1); // Remove the trailing '0' to get the base URL

    console.log("editBlogId:", editBlogId);
    let method, url;
    if (editBlogId == undefined) {
      method = "POST";
      url = blogsUrl;
    }
    else{
      method = "PUT";
      url = `${blogUrl}${editBlogId}`
    }
    console.log("method:", method);
    console.log("url:", url);


    $.ajax({
      url: url,
      method: method ,
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

  // Handle blog deletion
  $("#deleteblog").on("click", function (e) {
    e.preventDefault();
    console.log("Delete blog button clicked");
    // Ask confirmation from user
    if (!confirm("Are you sure you want to delete this blog?")) {
      return;
    }
    var blogUrl = `${blogWithIdZero}`.slice(0, -1); // Remove the trailing '0' to get the base URL

    $.ajax({
      url: `${blogUrl}${editBlogId}`,
      method: "DELETE",
      contentType: "application/json",
      headers: {
        Authorization: localStorage.getItem("access_token"),
        Accept: "application/json",
      },
      // data: JSON.stringify({ title: title, content: content }),
      success: function () {
        $("#editBlogModal").modal("hide");
        fetchBlogs();
      },
    });
  });


});
