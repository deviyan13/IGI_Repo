import pandas as pd

def main():
    # Load dataset from CSV
    file_path = "Global_Cybersecurity_Threats_2015-2024.csv"
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return

    print("Информация о DataFrame:")
    print(df.info())
    print("\nПервые 5 строк DataFrame:")
    print(df.head())

    max_users = df["Number of Affected Users"].max()
    min_users = df["Number of Affected Users"].min()

    df_max = df[df["Number of Affected Users"] == max_users]
    df_min = df[df["Number of Affected Users"] == min_users]

    mean_loss_max = df_max["Financial Loss (in Million $)"].mean()
    mean_loss_min = df_min["Financial Loss (in Million $)"].mean()

    if mean_loss_min == 0:
        ratio = float('inf')
    else:
        ratio = mean_loss_max / mean_loss_min
    ratio = round(ratio, 2)

    print("\nОтношение среднего финансового ущерба (в миллионах долларов) для атак с максимальным числом затронутых пользователей")
    print("к фин. ущербу для атак с минимальным числом затронутых пользователей:", ratio)


    overall_avg_loss = df["Financial Loss (in Million $)"].mean()

    df_below = df[df["Financial Loss (in Million $)"] < overall_avg_loss]
    avg_resolution_time = df_below["Incident Resolution Time (in Hours)"].mean()
    avg_resolution_time = round(avg_resolution_time, 2)

    print("\nСреднее время устранения инцидентов (в часах) для атак с финансовым ущербом ниже среднего:",
          avg_resolution_time)

    print('\nСписок стран, отсортированных по суммарным потерям в миллионах долларов за 2015-2024 гг.')
    print(df.groupby('Country')['Financial Loss (in Million $)'].sum().sort_values(ascending=False))



if __name__ == '__main__':
    main()
