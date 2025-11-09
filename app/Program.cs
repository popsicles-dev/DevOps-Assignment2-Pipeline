using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace YourNamespace
{
    class Program
    {
        static async Task Main(string[] args)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri("http://localhost:5000/");

                var formData = new MultipartFormDataContent();
                formData.Add(new StringContent("value_for_kmdrive"), "kmdrive");
                formData.Add(new StringContent("value_for_avg"), "avg");
                formData.Add(new StringContent("value_for_byear"), "byear");
                formData.Add(new StringContent("value_for_type"), "type");

                HttpResponseMessage response = await client.PostAsync("carscorefunc", formData);

                if (response.IsSuccessStatusCode)
                {
                    string responseContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseContent);
                }
                else
                {
                    Console.WriteLine("Failed to make request. Status code: " + response.StatusCode);
                }
            }
        }
    }
}
