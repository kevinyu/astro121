f_sample = 200e6
filter_func = np.array([1, 1, 1, 0, 0, 0, 1, 1])
filter_time_domain = np.fft.ifft(filter_func)

plot(np.array([0, 1, 2, 3, -4, -3, -2, -1]), filter_time_domain.real, "bo")
plot(np.array([0, 1, 2, 3, -4, -3, -2, -1]), filter_time_domain.imag, "ro")

print "real coeffs"
for i in [4, 5, 6, 7, 0, 1, 2, 3]:
    to_convert = filter_time_domain.real[i]
    number = np.binary_repr(to_convert * 2**17, 18)
    print number, hex(int(number, 2))



print "imag coeffs"
for i in [4, 5, 6, 7, 0, 1, 2, 3]:
    print filter_time_domain.imag[i]
figure()

actual_time_domain_signal = list(filter_time_domain[4:]) + list(filter_time_domain[:4])

bleh = np.fft.fft(actual_time_domain_signal)
plot(np.fft.fftfreq(8, 1./f_sample), abs(bleh), "bo")
# plot(np.fft.fftfreq(8, 1./f_sample), bleh.imag, "ro")
