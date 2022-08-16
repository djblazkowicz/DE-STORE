using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using DE_BusinessLayer;

namespace DE_PresentationLayer
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public BusinessLayer businessLayer = new BusinessLayer();
        public List<Item> basket = new List<Item>();

        public int total = 0;

        public MainWindow()
        {
            InitializeComponent();

            //ClearComboBoxes();
            businessLayer.GetStoreList();
            businessLayer.GetUserList();
            businessLayer.GetArticleList();
            businessLayer.GetDealList(0);

            ListBoxArticles.ItemsSource = businessLayer.ArticleList;
            ListBoxArticles.DisplayMemberPath = "Name";

            ListBoxBasket.ItemsSource = basket;
            ListBoxBasket.DisplayMemberPath = "Name";

            ComboBoxUserList.ItemsSource = businessLayer.UserList;
            ComboBoxUserList.DisplayMemberPath = "Name";

            ComboBoxStoreList.ItemsSource = businessLayer.StoreList;
            ComboBoxStoreList.DisplayMemberPath = "Name";

            ListBoxStoreItems.ItemsSource = businessLayer.ItemList;
            ListBoxStoreItems.DisplayMemberPath = "Name";

        }

        public void ClearComboBoxes()
        {
            ComboBoxStoreList.Items.Clear();
            ComboBoxUserList.Items.Clear();
        }

        public void Go_Button_Action()
        {

        }

        public void LabelUserList_Action()
        {
            User user = businessLayer.UserList.ElementAt(ComboBoxUserList.SelectedIndex);
            LabelLoyaltyPoints.Content = "Loyalty Points: " + user.Points;
        }

        public void ComboBoxStoreList_Action()
        {
            Store store = businessLayer.StoreList.ElementAt(ComboBoxStoreList.SelectedIndex);
            businessLayer.GetItemList(store.id);
            ListBoxStoreItems.ItemsSource = businessLayer.ItemList;
            ListBoxStoreItems.DisplayMemberPath = "Name";

            ListBoxStoreItems.Items.Refresh();

            //ComboBoxUserList.ItemsSource = businessLayer.UserList;
            //ComboBoxUserList.DisplayMemberPath = "Name";
        }

        public void ButtonAddToBasket_Action()
        {
            Item item = businessLayer.ItemList.ElementAt(ListBoxStoreItems.SelectedIndex);

            Item basketitem = businessLayer.AddToBasket(item.id);

            basket.Add(basketitem);

            total = total + basketitem.Price;

            LabelTotalValue.Content = total;

            //ListBoxBasket.ItemsSource = basket;
            //ListBoxBasket.DisplayMemberPath = "Name";
            ListBoxBasket.Items.Refresh();

            Store store = businessLayer.StoreList.ElementAt(ComboBoxStoreList.SelectedIndex);
            businessLayer.GetItemList(store.id);
            ListBoxStoreItems.ItemsSource = businessLayer.ItemList;
            ListBoxStoreItems.DisplayMemberPath = "Name";

        }

        public void ButtonClearBasket_Action()
        {
            void removeFromBasket(int id)
            {
                basket = businessLayer.RemoveFromBasket(id, basket);
            }
            foreach (Item item in basket)
            {
                removeFromBasket(item.id);
            }
            basket.Clear();
            ListBoxBasket.Items.Refresh();

            Store store = businessLayer.StoreList.ElementAt(ComboBoxStoreList.SelectedIndex);
            businessLayer.GetItemList(store.id);
            ListBoxStoreItems.ItemsSource = businessLayer.ItemList;
            ListBoxStoreItems.DisplayMemberPath = "Name";

            total = 0;

            LabelTotalValue.Content = total;
        }

        public void ButtonPurchaseBasket_Action()
        {
            bool finance = false;
            if (CheckBoxFinance.IsChecked == true)
            {
                finance = true;
            }
            businessLayer.PurchaseBasket(basket, finance);

            basket.Clear();
            ListBoxBasket.Items.Refresh();

            Store store = businessLayer.StoreList.ElementAt(ComboBoxStoreList.SelectedIndex);
            businessLayer.GetItemList(store.id);
            ListBoxStoreItems.ItemsSource = businessLayer.ItemList;
            ListBoxStoreItems.DisplayMemberPath = "Name";

            total = 0;

            LabelTotalValue.Content = total;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {

        }

        private void ButtonGo_Click(object sender, RoutedEventArgs e)
        {
            Go_Button_Action();
        }

        private void ComboBoxUserList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            LabelUserList_Action();
        }

        private void ComboBoxStoreList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ComboBoxStoreList_Action();
        }

        private void ButtonAddToBasket_Click(object sender, RoutedEventArgs e)
        {
            ButtonAddToBasket_Action();
        }

        private void ListBoxStoreItems_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void ListBoxBasket_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void ButtonClearBasket_Click(object sender, RoutedEventArgs e)
        {
            ButtonClearBasket_Action();
        }

        private void ButtonPurchase_Click(object sender, RoutedEventArgs e)
        {
            ButtonPurchaseBasket_Action();
        }
    }
}
