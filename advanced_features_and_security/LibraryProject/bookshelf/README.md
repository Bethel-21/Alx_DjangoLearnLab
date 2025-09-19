

# Permissions and Groups Setup

## Custom Permissions
Defined in `Book` model:
- can_view → View books
- can_create → Create new books
- can_edit → Edit existing books
- can_delete → Delete books

## Groups
- Viewers → only can_view
- Editors → can_create, can_edit
- Admins → all permissions

## Views
Each view checks the required permission using `@permission_required`.
Example: 
- book_list → requires can_view
- book_create → requires can_create
- book_edit → requires can_edit
- book_delete → requires can_delete
