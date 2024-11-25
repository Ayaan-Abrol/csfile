import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, messagebox, simpledialog
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_csv():
    """ Load a CSV file using a file dialog. """
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "test.csv")])
    if file_path:
        logging.info(f"File selected: {file_path}")
        try:
            df = pd.read_csv(file_path)
            logging.info(f"File loaded successfully. Columns: {list(df.columns)}")
            return df
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            messagebox.showerror("Error", f"Could not load file: {e}")
            return None
    else:
        logging.info("No file selected.")
        return None

def save_csv(df):
    """ Save the current DataFrame to a new CSV file. """
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df.to_csv(file_path, index=False)
            logging.info(f"File saved successfully: {file_path}")
            messagebox.showinfo("Success", f"File saved successfully to {file_path}")
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        logging.info("Save operation canceled.")

def display_data_info(df):
    """ Display basic information about the DataFrame. """
    try:
        info_str = df.info(buf=None)
        print(info_str)
        logging.info("Displayed DataFrame information.")
    except Exception as e:
        logging.error(f"Error displaying DataFrame info: {e}")
        messagebox.showerror("Error", f"Could not display data info: {e}")

def describe_data(df):
    """ Show statistical summary of the DataFrame. """
    try:
        summary = df.describe()
        print(summary)
        messagebox.showinfo("Summary", "Statistical summary displayed in console.")
        logging.info("Displayed statistical summary.")
    except Exception as e:
        logging.error(f"Error displaying summary: {e}")
        messagebox.showerror("Error", f"Could not display summary: {e}")

def handle_missing_data(df):
    """ Handle missing data by allowing the user to drop or fill missing values. """
    action = simpledialog.askstring(
        "Missing Data",
        "Choose action for missing data (drop, fill, cancel):",
    )
    if action == "drop":
        df.dropna(inplace=True)
        logging.info("Missing data rows dropped.")
        messagebox.showinfo("Success", "Rows with missing data were dropped.")
    elif action == "fill":
        fill_value = simpledialog.askstring(
            "Fill Missing Data", "Enter value to fill missing data:"
        )
        try:
            df.fillna(fill_value, inplace=True)
            logging.info(f"Missing data filled with {fill_value}.")
            messagebox.showinfo("Success", f"Missing data filled with '{fill_value}'.")
        except Exception as e:
            logging.error(f"Error filling missing data: {e}")
            messagebox.showerror("Error", f"Could not fill missing data: {e}")
    elif action == "cancel":
        logging.info("Missing data handling canceled.")
    else:
        logging.warning("Invalid input for missing data handling.")

def plot_simple(df):
    """ Plot a simple line plot of all numerical columns. """
    try:
        df.plot()
        plt.title("Simple Plot of All Numerical Columns")
        plt.xlabel("Index")
        plt.ylabel("Values")
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting data: {e}")
        messagebox.showerror("Error", f"Could not plot data: {e}")

def plot_pairplot(df):
    """ Plot a pairplot using seaborn for better visualization of relationships. """
    try:
        sns.pairplot(df)
        plt.suptitle("Pairplot of DataFrame", y=1.02)
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting pairplot: {e}")
        messagebox.showerror("Error", f"Could not plot pairplot: {e}")

def plot_histogram(df):
    """ Plot histograms of all numerical columns. """
    try:
        df.hist(bins=20, figsize=(20, 15))
        plt.suptitle("Histograms of Numerical Columns")
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting histograms: {e}")
        messagebox.showerror("Error", f"Could not plot histograms: {e}")

def plot_heatmap(df):
    """ Plot a heatmap of correlations between numerical columns. """
    try:
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", linewidths=0.5)
        plt.title("Heatmap of Correlations")
        plt.show()
    except Exception as e:
        logging.error(f"Error plotting heatmap: {e}")
        messagebox.showerror("Error", f"Could not plot heatmap: {e}")

def filter_data(df):
    """ Filter data by a column and value. """
    column = simpledialog.askstring("Filter", "Enter column name to filter:")
    if column not in df.columns:
        messagebox.showerror("Error", "Column not found.")
        return df
    value = simpledialog.askstring("Filter", f"Enter value to filter {column}:")
    try:
        filtered_df = df[df[column] == value]
        logging.info(f"Data filtered on {column} = {value}.")
        print(filtered_df)
        return filtered_df
    except Exception as e:
        logging.error(f"Error filtering data: {e}")
        messagebox.showerror("Error", f"Could not filter data: {e}")
        return df

def user_plot_selection(df):
    """ Allow the user to select the type of plot. """
    while True:
        plot_type = simpledialog.askstring(
            "Input", "Enter plot type (simple, pairplot, histogram, heatmap, exit):"
        )
        if plot_type == "simple":
            plot_simple(df)
        elif plot_type == "pairplot":
            plot_pairplot(df)
        elif plot_type == "histogram":
            plot_histogram(df)
        elif plot_type == "heatmap":
            plot_heatmap(df)
        elif plot_type == "exit":
            break
        else:
            messagebox.showwarning("Invalid input", "Please enter a valid plot type.")

def main():
    logging.info("Application started.")
    df = load_csv()
    if df is not None:
        while True:
            action = simpledialog.askstring(
                "Action",
                "Choose an action (info, summary, missing, filter, save, plot, exit):",
            )
            if action == "info":
                display_data_info(df)
            elif action == "summary":
                describe_data(df)
            elif action == "missing":
                handle_missing_data(df)
            elif action == "filter":
                df = filter_data(df)
            elif action == "save":
                save_csv(df)
            elif action == "plot":
                user_plot_selection(df)
            elif action == "exit":
                break
            else:
                messagebox.showwarning("Invalid input", "Please enter a valid action.")
    logging.info("Application ended.")

if __name__ == "__main__":
    main()
