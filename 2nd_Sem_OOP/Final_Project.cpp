#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>

using namespace std;

class MenuItem {
public:
    string name;
    float price;

    MenuItem() {
        name = "";
        price = 0.0;
    }

    MenuItem(string n, float p) {
        name = n;
        price = p;
    }
};

class Order {
public:
    string customerName;
    int tableNo;
    MenuItem items[50];
    int quantities[50];
    int itemCount;

    Order() {
        customerName = "";
        tableNo = 0;
        itemCount = 0;
    }

    void addItem(MenuItem item, int quantity) {
        if (itemCount < 50) {
            items[itemCount] = item;
            quantities[itemCount] = quantity;
            itemCount++;
        } else {
            cout << "Order limit reached!" << endl;
        }
    }

    float getTotalPrice() {
        float total = 0.0f;
        for (int i = 0; i < itemCount; ++i) {
            total += items[i].price * quantities[i];
        }
        return total;
    }
};

class Restaurant {
private:
    Order orders[50];
    int orderCount;

public:
    Restaurant() {
        orderCount = 0;
    }

    void addOrder() {
        if (orderCount >= 50) {
            cout << "Order limit reached!" << endl;
            return;
        }

        Order newOrder;
        cout << "Enter customer name: ";
        cin >> newOrder.customerName;
        cout << "Enter table number: ";
        cin >> newOrder.tableNo;

        int choice;
        do {
            displayMenu();
            cout << "Enter item number to add to order: ";
            int itemNumber;
            cin >> itemNumber;
            cout << "Enter quantity: ";
            int quantity;
            cin >> quantity;

            MenuItem item = getMenuItem(itemNumber);
            newOrder.addItem(item, quantity);

            cout << "Add another item? (1 for Yes, 0 for No): ";
            cin >> choice;
        } while (choice != 0);

        orders[orderCount] = newOrder;
        orderCount++;
        saveOrdersToFile();
    }

    void editOrder() {
        int orderNumber;
        cout << "Enter order number to edit: ";
        cin >> orderNumber;

        if (orderNumber <= 0 || orderNumber > orderCount) {
            cout << "Invalid order number!" << endl;
            return;
        }

        Order &order = orders[orderNumber - 1];
        cout << "Editing order for " << order.customerName << " at table " << order.tableNo << endl;

        int choice;
        do {
            displayMenu();
            cout << "Enter item number to add to order: ";
            int itemNumber;
            cin >> itemNumber;
            cout << "Enter quantity: ";
            int quantity;
            cin >> quantity;

            MenuItem item = getMenuItem(itemNumber);
            order.addItem(item, quantity);

            cout << "Add another item? (1 for Yes, 0 for No): ";
            cin >> choice;
        } while (choice != 0);

        saveOrdersToFile();
    }

    void deleteOrder() {
        int orderNumber;
        cout << "Enter order number to delete: ";
        cin >> orderNumber;

        if (orderNumber <= 0 || orderNumber > orderCount) {
            cout << "Invalid order number!" << endl;
            return;
        }

        for (int i = orderNumber - 1; i < orderCount - 1; ++i) {
            orders[i] = orders[i + 1];
        }
        orderCount--;
        saveOrdersToFile();
    }

    void viewOrders() {
        if (orderCount == 0) {
            cout << "No orders available!" << endl;
            return;
        }

        for (int i = 0; i < orderCount; ++i) {
            cout << "Order #" << i + 1 << " for " << orders[i].customerName << " at table " << orders[i].tableNo << endl;
            for (int j = 0; j < orders[i].itemCount; ++j) {
                cout << orders[i].items[j].name << " x" << orders[i].quantities[j] << " = Rs" << orders[i].items[j].price * orders[i].quantities[j] << endl;
            }
            cout << "Total: Rs" << orders[i].getTotalPrice() << endl;
            cout << "---------------------------------" << endl;
        }
    }

    void generateBill() {
        int orderNumber;
        cout << "Enter order number to generate bill: ";
        cin >> orderNumber;

        if (orderNumber <= 0 || orderNumber > orderCount) {
            cout << "Invalid order number!" << endl;
            return;
        }

        Order &order = orders[orderNumber - 1];
        cout << "Bill for " << order.customerName << " at table " << order.tableNo << endl;

        for (int i = 0; i < order.itemCount; ++i) {
            cout << order.items[i].name << " x" << order.quantities[i] << " = Rs" << order.items[i].price * order.quantities[i] << endl;
        }
        cout << "Total: Rs" << order.getTotalPrice() << endl;
        cout << "=================================" << endl;
    }

private:
    void displayMenu() {
        cout << "Menu:\n"
             << "1. Chicken Momo - Rs.220\n"
             << "2. Veg Momo - Rs.180\n"
             << "3. Paneer Momo - Rs.250\n"
             << "4. Ham Burger - Rs.340\n"
             << "5. Veg Burger - Rs.200\n"
             << "6. Chicken Burger - Rs.280\n"
             << "7. Pepperoni Pizza - Rs.720\n"
             << "8. Veg Pizza - Rs.620\n"
             << "9. Chicken Pizza - Rs.680\n"
             << "10. Vanilla Ice Cream - Rs.240\n"
             << "11. Chocolate Ice Cream - Rs.240\n"
             << "12. Strawberry Ice Cream - Rs.240\n"
             << "13. Coke - Rs.80\n"
             << "14. Lemonade - Rs.100\n"
             << "15. Iced Tea - Rs.120\n"
             << "16. French Fries - Rs.150\n"
             << "17. Onion Rings - Rs.180\n"
             << "18. Garlic Bread - Rs.200\n"
             << "19. Chocolate Cake - Rs.300\n"
             << "20. Brownie - Rs.280" << endl;
    }

    MenuItem getMenuItem(int itemNumber) {
        switch (itemNumber) {
            case 1: return MenuItem("Chicken Momo", 220);
            case 2: return MenuItem("Veg Momo", 180);
            case 3: return MenuItem("Paneer Momo", 250);
            case 4: return MenuItem("Ham Burger", 340);
            case 5: return MenuItem("Veg Burger", 200);
            case 6: return MenuItem("Chicken Burger", 280);
            case 7: return MenuItem("Pepperoni Pizza", 720);
            case 8: return MenuItem("Veg Pizza", 620);
            case 9: return MenuItem("Chicken Pizza", 680);
            case 10: return MenuItem("Vanilla Ice Cream", 240);
            case 11: return MenuItem("Chocolate Ice Cream", 240);
            case 12: return MenuItem("Strawberry Ice Cream", 240);
            case 13: return MenuItem("Coke", 80);
            case 14: return MenuItem("Lemonade", 100);
            case 15: return MenuItem("Iced Tea", 120);
            case 16: return MenuItem("French Fries", 150);
            case 17: return MenuItem("Onion Rings", 180);
            case 18: return MenuItem("Garlic Bread", 200);
            case 19: return MenuItem("Chocolate Cake", 300);
            case 20: return MenuItem("Brownie", 280);
            default: return MenuItem("Unknown", 0);
        }
    }

    void saveOrdersToFile() {
        ofstream file("orders.txt");
        for (int i = 0; i < orderCount; ++i) {
            file << orders[i].customerName << "," << orders[i].tableNo << ",";
            for (int j = 0; j < orders[i].itemCount; ++j) {
                file << orders[i].items[j].name << "," << orders[i].quantities[j] << ",";
            }
            file << orders[i].getTotalPrice() << endl;
        }
        file.close();
    }
};

int main() {
    Restaurant restaurant;
    int choice;

    while (true) {
        cout << "1. Add Order\n"
             << "2. Edit Order\n"
             << "3. Delete Order\n"
             << "4. View Orders\n"
             << "5. Generate Bill\n"
             << "6. Exit\n"
             << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                restaurant.addOrder();
                break;
           
            case 2:
                restaurant.editOrder();
                break;

            case 3:
                restaurant.deleteOrder();
                break;

            case 4:
                restaurant.viewOrders();
                break;

            case 5:
                restaurant.generateBill();
                break;

            case 6:
                cout << "Exiting the program. Thank you!" << endl;
                return 0;

            default:
                cout << "Invalid choice! Please try again." << endl;
                break;
        }
    }

    return 0;
}
