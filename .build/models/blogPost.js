"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BlogPost = void 0;
var uuid_1 = require("uuid");
var BlogPost = /** @class */ (function () {
    function BlogPost(title, content, author, id, updatedAt, createdAt) {
        this.id = id || (0, uuid_1.v4)();
        this.title = title;
        this.content = content;
        this.author = author;
        this.createdAt = createdAt || new Date().toISOString();
        this.updatedAt = updatedAt || new Date().toISOString();
    }
    BlogPost.prototype.publish = function () {
        // Logic to publish the blog post
        console.log("\"".concat(this.title, "\" by ").concat(this.author, " has been published."));
    };
    return BlogPost;
}());
exports.BlogPost = BlogPost;
//# sourceMappingURL=blogPost.js.map