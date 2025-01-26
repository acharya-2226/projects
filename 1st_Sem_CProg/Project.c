#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_EMPLOYEES 100
#define FILE_NAME "employees.csv"

typedef struct {
    int empID;
    char name[50];
    char contactNo[15];
    char address[100];
    char post[50];
    char email[50];
    float salary;
} Employee;

Employee employees[MAX_EMPLOYEES];
int numEmployees = 0;

void createNewFile() {
    FILE *file = fopen(FILE_NAME, "w");
    if (file == NULL) {
        printf("Error creating file.\n");
        return;
    }
    fprintf(file, "EmpID,Name,Contact No.,Address,Post,Email,Salary\n");
    fclose(file);
    printf("New file created successfully.\n");
}

void readFile() {
    FILE *file = fopen(FILE_NAME, "r");
    if (file == NULL) {
        printf("File not found.\n");
        return;
    }
    char line[256];
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }
    fclose(file);
}

void appendFile() {
    FILE *file = fopen(FILE_NAME, "a");
    if (file == NULL) {
        printf("Error opening file.\n");
        return;
    }
    for (int i = 0; i < numEmployees; i++) {
        fprintf(file, "%d,%s,%s,%s,%s,%s,%.2f\n",
                employees[i].empID, employees[i].name, employees[i].contactNo,
                employees[i].address, employees[i].post, employees[i].email,
                employees[i].salary);
    }
    fclose(file);
    printf("Data appended to file successfully.\n");
}

void addEmployee() {
    if (numEmployees >= MAX_EMPLOYEES) {
        printf("Maximum number of employees reached.\n");
        return;
    }
    Employee emp;
    printf("Enter EMP ID: ");
    scanf("%d", &emp.empID);
    printf("Enter Name: ");
    scanf("%s", emp.name);
    printf("Enter Contact No.: ");
    scanf("%s", emp.contactNo);
    printf("Enter Address: ");
    scanf("%s", emp.address);
    printf("Enter Post: ");
    scanf("%s", emp.post);
    printf("Enter Email: ");
    scanf("%s", emp.email);
    printf("Enter Salary: ");
    scanf("%f", &emp.salary);
    
    employees[numEmployees++] = emp;
    printf("Employee added successfully.\n");
}

void editEmployee(int empID) {
    for (int i = 0; i < numEmployees; i++) {
        if (employees[i].empID == empID) {
            printf("Enter new Name: ");
            scanf("%s", employees[i].name);
            printf("Enter new Contact No.: ");
            scanf("%s", employees[i].contactNo);
            printf("Enter new Address: ");
            scanf("%s", employees[i].address);
            printf("Enter new Post: ");
            scanf("%s", employees[i].post);
            printf("Enter new Email: ");
            scanf("%s", employees[i].email);
            printf("Enter new Salary: ");
            scanf("%f", &employees[i].salary);
            printf("Employee details updated successfully.\n");
            return;
        }
    }
    printf("Employee not found.\n");
}

void deleteEmployee(int empID) {
    int found = 0;
    for (int i = 0; i < numEmployees; i++) {
        if (employees[i].empID == empID) {
            found = 1;
            for (int j = i; j < numEmployees - 1; j++) {
                employees[j] = employees[j + 1];
            }
            numEmployees--;
            printf("Employee deleted successfully.\n");
            break;
        }
    }
    if (!found) {
        printf("Employee not found.\n");
    }
}

void generateQuery(int empID) {
    printf("EmpID\tName\tContact No.\tAddress\tPost\tEmail\tSalary\n");
    for (int i = 0; i < numEmployees; i++) {
        if (employees[i].empID == empID) {
            printf("%d\t%s\t%s\t%s\t%s\t%s\t%.2f\n",
                   employees[i].empID, employees[i].name, employees[i].contactNo,
                   employees[i].address, employees[i].post, employees[i].email,
                   employees[i].salary);
            return;
        }
    }
    printf("Employee not found.\n");
}

int main() {
    int choice, empID;
    
    do {
        printf("\nEmployee Management System Menu\n");
        printf("1. Create a new File\n");
        printf("2. Read a file\n");
        printf("3. Append the file\n");
        printf("4. Add an employee\n");
        printf("5. Edit specific records given employee ID\n");
        printf("6. Delete a certain record of an employee\n");
        printf("7. Generate a query for an employee\n");
        printf("8. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                createNewFile();
                break;
            case 2:
                readFile();
                break;
            case 3:
                appendFile();
                break;
            case 4:
                addEmployee();
                break;
            case 5:
                printf("Enter employee ID to edit: ");
                scanf("%d", &empID);
                editEmployee(empID);
                break;
            case 6:
                printf("Enter employee ID to delete: ");
                scanf("%d", &empID);
                deleteEmployee(empID);
                break;
            case 7:
                printf("Enter employee ID to generate query: ");
                scanf("%d", &empID);
                generateQuery(empID);
                break;
            case 8:
                printf("Exiting the program...\n");
                break;
            default:
                printf("Invalid choice! Please enter a number between 1 and 8.\n");
        }
    } while (choice != 8);

    return 0;
}
