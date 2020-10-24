class Thermo {
    public:
      void init(int gpioPin);
      double getData();
    private:
      int spiDevice;
      int enablePin;
};
