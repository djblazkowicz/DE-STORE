using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.Json.Nodes;

namespace DE_BusinessLayer
{
    public class BusinessLayer
    {

        public IEnumerable<Store> StoreList;
        public IEnumerable<User> UserList;
        public IEnumerable<Article> ArticleList;


        public IEnumerable<StockTransfer> StockTransferList;

        public List<Deal> DealList;
        public List<PurchaseOrder> PurchaseOrderList;
        public PurchaseOrder CurrentPurchaseOrder;

        public List<Item> ItemList;

        const string URL = "http://127.0.0.1:5000/";
        public HttpClient client = new HttpClient();
        

        public BusinessLayer()
        {
            client.BaseAddress = new Uri(URL);
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }
        
        
        public void GetStoreList()
        {
            JsonObject obj = new JsonObject();
            
            obj.Add("SQL", "select * from store_model");
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            StoreList = result.Content.ReadAsAsync<IEnumerable<Store>>().Result;
        }

        public void GetUserList()
        {
            JsonObject obj = new JsonObject();

            obj.Add("SQL", "select * from user_model");
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            UserList = result.Content.ReadAsAsync<IEnumerable<User>>().Result;
        }

        public void GetArticleList()
        {
            JsonObject obj = new JsonObject();

            obj.Add("SQL", "select * from article_model");
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            ArticleList = result.Content.ReadAsAsync<IEnumerable<Article>>().Result;
        }

        public void GetItemList(int id)
        {
            JsonObject obj = new JsonObject();

            string query = "select item_model.id,Article,Status,Store,StockTransfer,article_model.Name,article_model.Price from item_model inner join article_model on item_model.Article = article_model.id where status = 1 and item_model.store = " + id;

            obj.Add("SQL", query);
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            ItemList = result.Content.ReadAsAsync<List<Item>>().Result;
        }

        //helper function to find item index
        public int findItemIndex(int id,List<Item> list)
        {
            int index = -1;

            foreach (Item basketObject in list)
            {
                if (basketObject.id == id) { index = list.IndexOf(basketObject); }
            }

            return index;
        }

        public Item AddToBasket(int id)
        {

            int index = findItemIndex(id,ItemList);

            Item item = ItemList.ElementAt(index);
    
            ItemList.ElementAt(index).SetStatus(2);

            JsonObject obj = new JsonObject();
            string query = "UPDATE item_model SET Status = 2 where id = " + id;
            obj.Add("SQL", query);
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            return item;
        }

        public List<Item> RemoveFromBasket(int id,List<Item> basket)
        {
            int index = findItemIndex(id,basket);

            Item item = basket.ElementAt(index);

            basket.ElementAt(index).SetStatus(1);

            JsonObject obj = new JsonObject();
            string query = "UPDATE item_model SET Status = 1 where id = " + id;
            obj.Add("SQL", query);
            string requestURL = URL + "SQLiteAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PostAsync(requestURL, content).Result;

            //basket.Remove(item);

            return basket;
        }

        public void CreatePurchaseOrder(int UserID, int Status, int PaymentMethod)
        {

            //generate new PO
            string date = DateTime.Now.ToString("yyyyMMdd", System.Globalization.CultureInfo.InvariantCulture);
            JsonObject obj = new JsonObject();
            obj.Add("Status", Status);
            obj.Add("PaymentMethod", PaymentMethod);
            obj.Add("Date", date);
            obj.Add("User", UserID);
            string requestURL = URL + "PurchaseOrderAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PutAsync(requestURL, content).Result;

            CurrentPurchaseOrder = result.Content.ReadAsAsync<PurchaseOrder>().Result;

            //update local PO list
            GetPurchaseOrderList(0);
        }

        public void PurchaseBasket(List<Item> basket, bool finance)
        {
            int status = 4;
            if (finance) { status = 3; }
            int payment = 1;
            if (finance) { payment = 2; }
            CreatePurchaseOrder(1, 1, payment);
            foreach (Item item in basket)
            {
                item.SetStatus(4);
                JsonObject obj = new JsonObject();
                string query = "UPDATE item_model SET Status = " + status +" where id = " + item.id;
                obj.Add("SQL", query);
                string requestURL = URL + "SQLiteAPI";
                var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
                var result = client.PostAsync(requestURL, content).Result;
                CreateItemPurchase(item);
            }
            CurrentPurchaseOrder = null;
        }

        public void CreateItemPurchase(Item item)
        {
            JsonObject obj = new JsonObject();
            obj.Add("PurchaseOrder", CurrentPurchaseOrder.id);
            obj.Add("Item", item.id);
            string requestURL = URL + "BasketAPI";
            var content = new StringContent(obj.ToString(), Encoding.UTF8, "application/json");
            var result = client.PutAsync(requestURL, content).Result;
        }

        public void GetPurchaseOrderList(int id)
        {
            string urlParameters = "GetPurchaseOrder/" + id;
            HttpResponseMessage response = client.GetAsync(urlParameters).Result;
            if (response.IsSuccessStatusCode)
            {
                PurchaseOrderList = response.Content.ReadAsAsync<List<PurchaseOrder>>().Result;
            }
        }

        public void GetStockTransferList(int id)
        {
            string urlParameters = "GetStockTransfer/" + id;
            HttpResponseMessage response = client.GetAsync(urlParameters).Result;
            if (response.IsSuccessStatusCode)
            {
                StockTransferList = response.Content.ReadAsAsync<IEnumerable<StockTransfer>>().Result;
            }
        }
        public void GetDealList(int id)
        {
            string urlParameters = "GetDeal/" + id;
            HttpResponseMessage response = client.GetAsync(urlParameters).Result;
            if (response.IsSuccessStatusCode)
            {
                DealList = response.Content.ReadAsAsync<List<Deal>>().Result;
            }
        }
    }
}
