import ditto_backend

print("RUNNING TEST...\n")

print("Current test: get_user_dir_path(1)")
print(ditto_backend.get_user_dir_path(1) + "\n")

print("Current test: creating libraries for user 1")
print(ditto_backend.create_lib(1, "dogs"))
print(ditto_backend.create_lib(1, "cats"))
print(ditto_backend.create_lib(1, "bats"))

print("Current test: get_user_dir_path(4)")
print(ditto_backend.get_user_dir_path(4) + "\n")

print("Current test: get_user_libs(1) Expected: Valid Output")
print(ditto_backend.get_user_libs(1))

print("Current test: get_user_libs(3)")
print(ditto_backend.get_user_libs(3))

print("Testing Library Creation")
print(ditto_backend.create_lib(3, "dogs"))
print(ditto_backend.create_lib(4, "dogs"))

print("Testing failed media retrieval")
print(ditto_backend.get_lib_image(1, "dogs", "cat"))

print("Testing media download")
print(ditto_backend.add_img_to_lib(1, "dogs", "d1", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))
print(ditto_backend.add_img_to_lib(3, "dogs", "d1", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))
print(ditto_backend.add_img_to_lib(3, "dogs", "d2", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))
print(ditto_backend.add_img_to_lib(3, "dogs", "d3", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))
print(ditto_backend.add_img_to_lib(3, "dogs", "d4", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))

print(ditto_backend.add_img_to_lib(4, "dogs", "d1", "https://cdn.discordapp.com/attachments/592776695069671424/593794343568015382/0.jpeg"))


print("Testing library images")
print(ditto_backend.get_lib_images(3,"dogs"))

print("Testing successful media retrieval")
print(ditto_backend.get_lib_image(1, "dogs", "d1"))

print("Testing random")
print(ditto_backend.get_random_image(1, "dogs"))
print(ditto_backend.get_random_image(3, "dogs"))

print("Testing image remove")
print(ditto_backend.remove_image(1, "dogs", "d1"))

print("Testing library remove")
print(ditto_backend.remove_lib(3, "dogs"))